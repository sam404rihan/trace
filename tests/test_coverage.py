import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402
from technique_coverage import check_coverage  # noqa: E402

TECH = {"t.x": {"name": "X", "explain": "x"}, "t.y": {"name": "Y", "explain": "y"}}


def course(*topics):
    """topics: (topic_id, [(name, kind, difficulty, uses, teaches), ...]) in course order."""
    tl, probs = [], {}
    for tid, items in topics:
        tl.append({"id": tid, "items": [i[0] for i in items]})
        for name, kind, diff, uses, teaches in items:
            probs[name] = {"kind": kind, "difficulty": diff, "uses": uses, "teaches": teaches,
                           "audited": True, "topic_id": tid}
    return tl, probs


GOOD = course(("01_a", [("snip", "snippet", "", [], ["t.x"]), ("teach_y", "solo", "easy", ["t.x"], ["t.y"]),
                        ("user", "solo", "medium", ["t.x", "t.y"], [])]),
              ("02_b", [("later", "solo", "hard", ["t.y"], [])]))


def run(c, tech=TECH):
    return check_coverage(c[0], c[1], tech)


class Rules(unittest.TestCase):
    def test_good_course_passes(self):
        self.assertEqual(run(GOOD), ([], []))

    def test_unknown_id(self):
        c = course(("01_a", [("p", "solo", "easy", ["t.zzz"], ["t.x", "t.y"])]))
        self.assertTrue(any("t.zzz" in e and "techniques.py" in e for e in run(c)[0]))

    def test_technique_without_teacher(self):
        c = course(("01_a", [("p", "solo", "easy", [], ["t.x"])]))
        self.assertTrue(any(e.startswith("t.y: no problem teaches it") for e in run(c)[0]))

    def test_two_teachers(self):
        c = course(("01_a", [("p", "solo", "easy", [], ["t.x", "t.y"]), ("q", "snippet", "", [], ["t.x"])]))
        self.assertTrue(any(e.startswith("t.x: taught by") for e in run(c)[0]))

    def test_teacher_must_be_basic(self):
        c = course(("01_a", [("p", "solo", "medium", [], ["t.x", "t.y"])]))
        self.assertTrue(any("p: teaches t.x" in e and "medium" in e for e in run(c)[0]))

    def test_teacher_later_in_same_topic(self):
        c = course(("01_a", [("snip", "snippet", "", ["t.x"], ["t.y"]), ("teach", "solo", "easy", [], ["t.x"])]))
        self.assertIn("snip uses t.x, but its teacher teach comes later in the same topic", run(c)[0])

    def test_teacher_in_later_topic(self):
        c = course(("01_a", [("p", "solo", "hard", ["t.x"], []), ("t", "snippet", "", [], ["t.y"])]),
                   ("02_b", [("q", "snippet", "", [], ["t.x"])]))
        self.assertIn("p uses t.x, but its teacher q comes in a later topic", run(c)[0])

    def test_earlier_topic_teacher_is_fine(self):
        self.assertFalse([e for e in run(GOOD)[0] if "later" in e])

    def test_cycle_is_an_error(self):
        c = course(("01_a", [("a", "solo", "easy", ["t.y"], ["t.x"]), ("b", "solo", "easy", ["t.x"], ["t.y"])]))
        self.assertTrue(any("comes later in the same topic" in e for e in run(c)[0]))

    def test_same_id_taught_and_used(self):
        c = course(("01_a", [("p", "solo", "easy", ["t.x"], ["t.x", "t.y"])]))
        self.assertIn("p: t.x is in both TEACHES and USES", run(c)[0])

    def test_tags_must_be_lists_of_ids(self):
        c = course(("01_a", [("p", "solo", "easy", "t.x", ["t.x", "t.y"])]))
        self.assertIn("p: USES must be a list of technique ids", run(c)[0])

    def test_unaudited_is_an_error(self):
        c = course(("01_a", [("snip", "snippet", "", [], ["t.x", "t.y"]), ("old", "solo", "hard", [], [])]))
        c[1]["old"]["audited"] = False
        errors, warnings = run(c)
        self.assertEqual(errors, ["old (01_a): not audited: give it a USES list"])
        self.assertEqual(warnings, [])


class RealCourse(unittest.TestCase):
    def test_no_coverage_errors(self):
        topics, problems = server.load_course()
        errors, _ = check_coverage(topics, problems, server.parse_techniques(server.TECHNIQUES_FILE))
        self.assertEqual(errors, [])

    def test_uses_are_in_teaching_order(self):
        # The in-topic lock names the first unsolved teacher in USES, so USES follows course order.
        topics, problems = server.load_course()
        pos = {n: i for i, n in enumerate(n for t in topics for n in t["items"])}
        teacher = {t: n for n, p in problems.items() for t in p["teaches"]}
        wrong = [n for n, p in problems.items() if p["uses"] != sorted(p["uses"], key=lambda t: pos[teacher[t]])]
        self.assertEqual(wrong, [])


class GraphTraversalPilot(unittest.TestCase):
    def setUp(self):
        self.topics, self.problems = server.load_course()
        self.topic = next(t for t in self.topics if t["id"] == "19_graph_traversal")

    def test_every_problem_is_audited(self):
        self.assertEqual([n for n in self.topic["items"] if not self.problems[n]["audited"]], [])

    def test_teachers_come_before_their_users(self):
        items = self.topic["items"]
        for teacher, user in (("flood_fill", "count_enclosed"), ("flood_fill", "num_islands"),
                              ("num_islands", "max_area_island"), ("count_enclosed", "pacific_atlantic"),
                              ("key_then_exit", "shortest_path_all_keys"), ("route_to_exit", "solve_maze")):
            self.assertLess(items.index(teacher), items.index(user), (teacher, user))

    def test_new_basics_are_easy(self):
        for name in ("reachable_nodes", "count_enclosed", "fewest_steps", "key_then_exit", "route_to_exit", "num_islands"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)

    def test_uses_lists_every_technique_used_directly(self):
        expected = {
            "rotting_oranges": {"bfs.multi_source", "bfs.shortest", "grid.neighbors"},
            "max_area_island": {"graph.components", "dfs.flood_fill", "grid.neighbors"},
            "pacific_atlantic": {"flood.from_targets", "dfs.flood_fill", "grid.neighbors"},
            "surrounded_regions": {"flood.from_targets", "dfs.flood_fill", "grid.neighbors"},
            "word_ladder": {"bfs.implicit", "bfs.shortest"},
            "shortest_path_all_keys": {"bfs.state", "bfs.shortest", "grid.neighbors"},
            "solve_maze": {"bfs.path", "bfs.shortest", "grid.neighbors"},
            "num_islands": {"dfs.flood_fill", "grid.neighbors"},
            "count_enclosed": {"dfs.flood_fill", "grid.neighbors"},
        }
        for name, uses in expected.items():
            self.assertEqual(set(self.problems[name]["uses"]), uses, name)

    def test_bus_routes_has_its_group_technique(self):
        self.assertIn("graph.groups", self.problems["bus_routes"]["uses"])
        self.assertEqual(self.problems["club_hops"]["teaches"], ["graph.groups"])
        items = self.topic["items"]
        self.assertLess(items.index("club_hops"), items.index("bus_routes"))

    def test_every_plan_item_exists(self):
        plans = server.load_plans()["plans"]
        missing = [n for pl in plans for s in pl["sections"] for n in s["items"] if n not in self.problems]
        self.assertEqual(missing, [])


STAGE_1 = ("01_big_o_in_practice", "02_python_toolkit", "03_arrays_and_strings", "04_hashing", "05_recursion")


class AuditBase(unittest.TestCase):
    """Helpers shared by the stage audits. Has no tests of its own."""

    @classmethod
    def setUpClass(cls):
        cls.topics, cls.problems = server.load_course()
        cls.by_id = {t["id"]: t for t in cls.topics}

    def items(self, topic_id):
        return self.by_id[topic_id]["items"]

    def assert_audited(self, topic_id):
        self.assertEqual([n for n in self.items(topic_id) if not self.problems[n]["audited"]], [], topic_id)

    def assert_uses(self, expected):
        for name, uses in expected.items():
            self.assertEqual(set(self.problems[name]["uses"]), set(uses), name)

    def assert_teaches(self, expected):
        for name, teaches in expected.items():
            self.assertEqual(self.problems[name]["teaches"], teaches, name)

    def cases_of(self, name):
        return server.load_module(next(server.COURSE.glob(f"*/*/{name}.py")))["TESTS"]


class Stage1Audit(AuditBase):
    """Part 2, Stage 1: topics 01-05 fully audited (docs/superpowers/plans/2026-10-16-technique-coverage-stage-1.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        for name, topic_id in (("max_profit", "01_big_o_in_practice"), ("min_k_bit_flips", "11_greedy"),
                               ("submatrix_sum_target", "08_prefix_sums"), ("concat_all_words", "07_sliding_window")):
            self.assertEqual(self.problems[name]["topic_id"], topic_id, name)

    def test_topics_01_and_02(self):
        self.assert_audited("01_big_o_in_practice")
        self.assert_audited("02_python_toolkit")
        self.assert_teaches({"common_count": ["hash.set_lookup"], "max_profit": ["scan.best_so_far"],
                             "best_sightseeing_pair": ["pairs.split_by_index"], "equal_pairs": ["hash.count_pairs"]})
        self.assert_uses({"common_elements": ["hash.set_lookup"], "best_sightseeing_pair": ["scan.best_so_far"],
                          "count_bad_pairs": ["hash.count_pairs", "pairs.split_by_index"],
                          "second_largest": ["scan.best_so_far"], "sum_pair_distances": [], "word_frequencies": []})
        for name in ("max_profit", "best_sightseeing_pair", "equal_pairs"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
        items = self.items("01_big_o_in_practice")
        self.assertLess(items.index("max_profit"), items.index("best_sightseeing_pair"))

    def test_topic_03(self):
        self.assert_audited("03_arrays_and_strings")
        self.assert_teaches({"rotate_index": ["array.wrap_index"], "spiral_order": ["matrix.boundaries"],
                             "move_zeroes": ["array.write_pointer"], "plus_one": ["math.carry"],
                             "distance_to_char": ["array.left_right_passes"]})
        self.assert_uses({"multiply_strings": ["math.carry"], "product_except_self": ["array.left_right_passes"],
                          "rotate_array": ["array.wrap_index"], "set_matrix_zeroes": ["hash.set_lookup"],
                          "max_chunks_to_sorted": ["array.left_right_passes", "scan.best_so_far"],
                          "detect_squares": ["hash.set_lookup"], "first_missing_positive": []})
        self.assertEqual(self.problems["distance_to_char"]["difficulty"], "easy")

    def test_topic_04(self):
        self.assert_audited("04_hashing")
        self.assert_teaches({"first_repeat": ["hash.seen_set"], "longest_consecutive": ["hash.run_starts"],
                             "two_sum": ["hash.complement"], "group_by_ends": ["hash.group_key"]})
        self.assert_uses({"contains_duplicate": ["hash.seen_set"], "is_happy": ["hash.seen_set"],
                          "is_valid_sudoku": ["hash.seen_set"], "group_anagrams": ["hash.group_key"],
                          "longest_consecutive": ["hash.set_lookup"],
                          "grid_illumination": ["hash.group_key", "hash.set_lookup"], "max_equal_freq": []})
        self.assertEqual(self.problems["group_by_ends"]["difficulty"], "easy")
        self.assertEqual(self.problems["grid_illumination"]["difficulty"], "hard")

    def test_topic_05(self):
        self.assert_audited("05_recursion")
        self.assert_teaches({"digit_sum": ["recursion.trust"], "count_paths": ["recursion.memo"],
                             "min_max_expr": ["recursion.parse"]})
        self.assert_uses({"scramble_string": ["recursion.memo", "recursion.trust"],
                          "calculate": ["recursion.parse", "recursion.trust"],
                          "count_of_atoms": ["recursion.parse", "recursion.trust"],
                          "flatten_list": ["recursion.trust"], "power": ["recursion.trust"],
                          "render_folders": ["recursion.trust"], "min_max_expr": ["recursion.trust"]})
        self.assertEqual(self.problems["min_max_expr"]["difficulty"], "easy")

    def test_every_stage_1_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_1:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        # Searching every c from every index is O(n * copies of c): many copies must be present.
        self.assertTrue(any(len(s) >= 100_000 and s.count(c) >= 10_000
                            for (s, c), _ in self.cases_of("distance_to_char")))
        # Counting each distinct value with nums.count is O(n * distinct values).
        self.assertTrue(any(len(nums) >= 100_000 and len(set(nums)) >= 10_000
                            for (nums,), _ in self.cases_of("equal_pairs")))

    def test_tags_stay_out_of_starters(self):
        leaks = [n for n, p in self.problems.items() if "USES" in p["starter"] or "TEACHES" in p["starter"]]
        self.assertEqual(leaks, [])



STAGE_2 = ("06_two_pointers", "07_sliding_window", "08_prefix_sums", "09_binary_search",
           "10_sorting_and_intervals", "11_greedy")


class Stage2Audit(AuditBase):
    """Part 2, Stage 2: topics 06-11 fully audited (docs/superpowers/plans/2026-10-17-technique-coverage-stage-2.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        for name in ("min_meeting_rooms", "min_interval_query"):
            self.assertEqual(self.problems[name]["topic_id"], "17_heaps", name)

    def test_topic_06(self):
        self.assert_audited("06_two_pointers")
        self.assert_teaches({"pointer_step": ["pointers.opposite_ends"], "is_subsequence": ["pointers.two_sequences"]})
        self.assert_uses({"remove_duplicates_sorted": ["array.write_pointer"],
                          "trap_rain_water": ["array.left_right_passes", "pointers.opposite_ends"],
                          "min_window_subsequence": ["pointers.two_sequences"],
                          "merge_logs": ["pointers.two_sequences"], "count_pairs_below": ["pointers.opposite_ends"]})
        self.assertEqual(self.problems["is_subsequence"]["difficulty"], "easy")


    def test_topic_07(self):
        self.assert_audited("07_sliding_window")
        self.assert_teaches({"slide_sum": ["window.fixed"], "longest_k_distinct": ["window.variable"],
                             "min_subarray_len": ["window.shortest"], "nice_subarrays": ["window.count"]})
        self.assert_uses({"check_inclusion": ["window.fixed"], "min_window": ["window.variable", "window.shortest"],
                          "subarrays_k_distinct": ["window.variable", "window.count"],
                          "concat_all_words": ["window.variable"], "rate_limiter": ["window.variable"]})
        for name in ("min_subarray_len", "nice_subarrays"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_08(self):
        self.assert_audited("08_prefix_sums")
        self.assert_teaches({"prefix_sums": ["prefix.sums"], "zero_sum_subarrays": ["prefix.count_dict"],
                             "range_additions": ["prefix.difference"]})
        self.assert_uses({"subarray_sum_equals_k": ["hash.complement", "prefix.sums", "prefix.count_dict"],
                          "submatrix_sum_target": ["prefix.sums", "prefix.count_dict"],
                          "min_moves_complementary": ["prefix.sums", "prefix.difference"],
                          "max_sum_three_subarrays": ["scan.best_so_far", "array.left_right_passes", "prefix.sums"]})
        for name in ("zero_sum_subarrays", "range_additions"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_09(self):
        self.assert_audited("09_binary_search")
        self.assert_teaches({"lower_bound": ["bsearch.first_true"], "ship_capacity": ["bsearch.on_answer"]})
        self.assert_uses({"split_array_largest_sum": ["bsearch.first_true", "bsearch.on_answer"],
                          "smallest_distance_pair": ["window.variable", "window.count", "bsearch.first_true",
                                                     "bsearch.on_answer"],
                          "sqrt_floor": ["bsearch.first_true", "bsearch.on_answer"],
                          "median_two_sorted": ["bsearch.first_true"], "time_map": ["bsearch.first_true"]})


    def test_topic_10(self):
        self.assert_audited("10_sorting_and_intervals")
        self.assert_teaches({"overlaps": ["intervals.overlap"], "insert_interval": ["intervals.merge"],
                             "can_attend_meetings": ["intervals.sort_by_start"],
                             "non_overlapping": ["intervals.earliest_end"]})
        self.assert_uses({"merge_intervals": ["intervals.overlap", "intervals.merge", "intervals.sort_by_start"],
                          "summary_ranges": ["bsearch.first_true", "intervals.merge"],
                          "range_module": ["bsearch.first_true", "intervals.overlap", "intervals.merge"],
                          "largest_number": []})
        self.assertEqual(self.problems["non_overlapping"]["difficulty"], "easy")

    def test_every_stage_2_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_2:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))


    def test_topic_11(self):
        self.assert_audited("11_greedy")
        self.assert_teaches({"extend_or_restart": ["greedy.kadane"], "min_jumps": ["greedy.farthest_reach"],
                             "min_suffix_flips": ["greedy.forced_first"]})
        self.assert_uses({"min_k_bit_flips": ["prefix.difference", "greedy.forced_first"],
                          "hand_of_straights": ["greedy.forced_first"], "gas_station": ["greedy.kadane"],
                          "min_taps": ["greedy.farthest_reach"], "candy": ["array.left_right_passes"],
                          "pick_talks": ["intervals.earliest_end"], "patching_array": [],
                          "valid_paren_string": ["brackets.balance"]})
        self.assert_teaches({"min_add_parens": ["brackets.balance"]})
        self.assertEqual(self.problems["min_add_parens"]["difficulty"], "easy")
        self.assertEqual(self.problems["min_suffix_flips"]["difficulty"], "easy")

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("is_subsequence", lambda st, w: len(st[0]) >= 1_000_000 and len(st[1]) >= 400_000)  # slicing s: O(n * m)
        big("min_add_parens", lambda a, w: a[0].startswith("(" * 100_000))                      # replace "()": O(n²)
        big("nice_subarrays", lambda a, w: len(a[0]) >= 100_000 and w >= 50_000_000)          # one step per answer
        big("zero_sum_subarrays", lambda a, w: len(a[0]) >= 100_000)                           # every subarray
        big("range_additions", lambda a, w: sum(r - l + 1 for l, r, _ in a[1]) >= 1_000_000_000)
        big("min_suffix_flips", lambda a, w: len(a[0]) >= 100_000 and w >= 50_000)            # flip per press
        big("min_subarray_len", lambda a, w: len(a[1]) >= 100_000 and w >= 10_000)            # every start
        big("non_overlapping", lambda a, w: len(a[0]) >= 20_000)                               # O(n²) DP


STAGE_3 = ("12_stacks", "13_queues_and_deques", "14_linked_lists", "15_trees", "16_binary_search_trees",
           "17_heaps", "18_tries")


class Stage3Audit(AuditBase):
    """Part 2, Stage 3: topics 12-18 fully audited (docs/superpowers/plans/2026-10-20-technique-coverage-stage-3.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        for name, topic_id in (("word_search_ii", "22_backtracking"), ("concatenated_words", "23_dynamic_programming_1d")):
            self.assertEqual(self.problems[name]["topic_id"], topic_id, name)


    def test_topic_12(self):
        self.assert_audited("12_stacks")
        self.assert_teaches({"bracket_step": ["stack.lifo"], "daily_temperatures": ["stack.monotonic"],
                             "largest_rectangle": ["stack.span"]})
        self.assert_uses({"car_fleet": ["scan.best_so_far"], "largest_rectangle": ["stack.monotonic"],
                          "maximal_rectangle": ["stack.monotonic", "stack.span"], "text_editor": ["stack.lifo"]})
        for name in ("daily_temperatures", "largest_rectangle"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_13(self):
        self.assert_audited("13_queues_and_deques")
        self.assert_teaches({"sliding_window_max": ["deque.monotonic"]})
        self.assert_uses({"max_value_of_equation": ["pairs.split_by_index", "window.variable", "deque.monotonic"],
                          "shortest_subarray_at_least_k": ["prefix.sums", "deque.monotonic"],
                          "expire_old": ["window.variable"], "ticket_queue": ["hash.set_lookup"]})
        self.assertEqual(self.problems["sliding_window_max"]["difficulty"], "easy")


    def test_topic_14(self):
        self.assert_audited("14_linked_lists")
        self.assert_teaches({"reverse_between": ["list.reverse", "list.dummy"], "middle_node": ["list.fast_slow"],
                             "recently_used": ["list.recency"], "cycle_start": ["list.cycle_start"]})
        self.assert_uses({"find_duplicate": ["list.fast_slow", "list.cycle_start"], "lfu_cache": ["list.recency"],
                          "merge_two_lists": ["pointers.two_sequences", "list.dummy"],
                          "sort_list": ["recursion.trust", "pointers.two_sequences", "sort.merge_count", "list.dummy",
                                        "list.fast_slow"]})
        for name in ("recently_used", "cycle_start"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_15(self):
        self.assert_audited("15_trees")
        self.assert_teaches({"count_nodes": ["tree.recursion"], "right_side_view": ["tree.bfs_levels"],
                             "diameter_of_tree": ["tree.return_and_record"], "has_path_sum": ["tree.carry_down"]})
        self.assert_uses({"max_path_sum": ["tree.return_and_record"], "min_cameras": ["tree.return_and_record"],
                          "good_nodes": ["tree.carry_down"], "serialize_tree": ["recursion.parse", "tree.recursion"],
                          "level_order": ["tree.bfs_levels"], "build_tree_pre_in": ["tree.recursion", "tree.inorder"]})
        self.assertEqual(self.problems["diameter_of_tree"]["difficulty"], "easy")
        self.assertEqual(self.problems["inorder_traversal"]["topic_id"], "15_trees")


    def test_topic_16(self):
        self.assert_audited("16_binary_search_trees")
        self.assert_teaches({"bst_insert": ["bst.walk_down"], "inorder_traversal": ["tree.inorder"]})
        self.assert_uses({"kth_smallest_bst": ["tree.inorder"], "closest_k_values": ["window.fixed", "tree.inorder"],
                          "max_sum_bst": ["tree.return_and_record"], "is_valid_bst": ["tree.carry_down"],
                          "tree_set": ["bst.walk_down", "tree.inorder"]})
        self.assertEqual(self.problems["inorder_traversal"]["difficulty"], "easy")


    def test_topic_17(self):
        self.assert_audited("17_heaps")
        self.assert_teaches({"push_keep_k": ["heap.top_k"], "last_stone": ["heap.max_negate"],
                             "median_finder": ["heap.two_heaps"], "max_bag": ["heap.lazy_delete"],
                             "k_smallest_sums": ["heap.k_way_merge"]})
        self.assert_uses({"sliding_window_median": ["window.fixed", "heap.max_negate", "heap.two_heaps", "heap.lazy_delete"],
                          "skyline": ["heap.max_negate", "heap.lazy_delete"],
                          "min_interval_query": ["intervals.sort_by_start", "heap.lazy_delete"],
                          "twitter": ["heap.max_negate", "heap.k_way_merge"], "merge_k_sorted": ["heap.k_way_merge"]})
        for name in ("median_finder", "max_bag", "k_smallest_sums"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
        self.assertEqual(self.problems["merge_k_sorted"]["difficulty"], "medium")


    def test_topic_18(self):
        self.assert_audited("18_tries")
        self.assert_teaches({"trie_insert": ["trie.walk"], "count_prefixes": []})
        self.assert_uses({"word_dictionary": ["recursion.trust", "trie.walk"], "count_prefixes": ["trie.walk"],
                          "stream_matches": ["trie.walk"], "palindrome_pairs": ["hash.complement"],
                          "autocomplete": ["bsearch.first_true"]})
        self.assertEqual(self.problems["count_prefixes"]["difficulty"], "medium")
        self.assertEqual(self.problems["stream_matches"]["difficulty"], "hard")

    def test_every_stage_3_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_3:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def removes_the_max(ops):
            gone = [op[1] for op in ops if op[0] == "remove"]
            return len(gone) >= 100_000 and all(x > y for x, y in zip(gone, gone[1:]))

        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("daily_temperatures", lambda a, w: len(a[0]) >= 100_000 and w.count(0) >= 50_000)   # look ahead: O(n²)
        big("daily_temperatures", lambda a, w: len(a[0]) >= 100_000 and w[0] == len(a[0]) - 1)  # ...even skipping hopeless days
        big("sliding_window_max", lambda a, w: len(a[0]) >= 100_000 and a[1] >= 50_000)          # max(): O(n * k)
        big("sliding_window_max", lambda a, w: len(a[0]) >= 100_000 and a[1] >= 50_000
            and all(x > y for x, y in zip(a[0], a[0][1:])))                                       # cached max: rescans
        big("largest_rectangle", lambda a, w: len(a[0]) >= 100_000
            and all(x < y for x, y in zip(a[0], a[0][1:])))                                       # widen each bar: O(n²)
        big("recently_used", lambda ops, w: len(ops) >= 200_000)                                 # list.remove: O(n)
        big("median_finder", lambda ops, w: sum(op[0] == "add_num" for op in ops) >= 250_000)    # insort: O(n)
        big("max_bag", lambda ops, w: len(ops) >= 300_000)                                       # max() or insort: O(n)
        big("max_bag", lambda ops, w: removes_the_max(ops))                                      # cached max: rescans
        big("k_smallest_sums", lambda a, w: min(len(a[0]), len(a[1]), a[2]) >= 100_000)          # k * k sums


STAGE_4 = ("20_topological_sort_and_union_find", "21_weighted_graphs", "22_backtracking",
           "23_dynamic_programming_1d", "24_dynamic_programming_2d", "25_bit_tricks")


class Stage4Audit(AuditBase):
    """Part 2, Stage 4: topics 20-25 fully audited (docs/superpowers/plans/2026-10-21-technique-coverage-stage-4.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        self.assertEqual(self.problems["largest_factor_component"]["topic_id"], "30_number_theory")


    def test_topic_20(self):
        self.assert_audited("20_topological_sort_and_union_find")
        self.assert_teaches({"find_root": ["uf.find"], "build_order": ["graph.topo_kahn"], "groups_after_each": ["uf.union"]})
        self.assert_uses({"course_schedule": ["graph.adjacency", "graph.topo_kahn"],
                          "redundant_connection": ["uf.find", "uf.union"], "network": ["uf.find", "uf.union"],
                          "parallel_courses_iii": ["graph.adjacency", "graph.topo_kahn"]})
        self.assertEqual(self.problems["groups_after_each"]["difficulty"], "easy")


    def test_topic_21(self):
        self.assert_audited("21_weighted_graphs")
        self.assert_teaches({"relax": ["sp.relax"], "cheapest_path": ["sp.dijkstra"], "mst_cost": ["graph.mst"],
                             "euler_path": ["graph.euler"], "bellman_ford": ["sp.bellman_ford"]})
        self.assert_uses({"cheapest_flights": ["sp.relax", "sp.bellman_ford"]})
        self.assert_uses({"min_cost_connect_points": ["heap.lazy_delete", "graph.mst"],
                          "reconstruct_itinerary": ["graph.euler"], "min_cost_in_time": ["bfs.state", "sp.dijkstra"],
                          "swim_rising_water": ["grid.neighbors", "sp.dijkstra"], "route_planner": ["bfs.path", "sp.dijkstra"]})
        for name in ("mst_cost", "euler_path", "bellman_ford"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_22(self):
        self.assert_audited("22_backtracking")
        self.assert_teaches({"combinations": ["bt.core"], "subsets_ii": ["bt.skip_duplicates"]})
        self.assert_uses({"combination_sum_ii": ["bt.core", "bt.skip_duplicates"],
                          "word_search_ii": ["trie.walk", "grid.neighbors", "bt.core"],
                          "n_queens": ["hash.group_key", "bt.core"], "generate_parentheses": ["brackets.balance", "bt.core"]})
        for name in ("subsets", "subsets_ii"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_23(self):
        self.assert_audited("23_dynamic_programming_1d")
        self.assert_teaches({"robber_step": ["dp.recurrence"], "decode_ways": ["dp.prefix"], "coin_change": ["dp.amounts"],
                             "longest_increasing_subsequence": ["dp.lis"], "palindromic_substrings": ["palin.expand"],
                             "partition_equal_subset": ["dp.knapsack01"]})
        self.assert_uses({"concatenated_words": ["trie.walk", "dp.prefix"], "russian_doll": ["dp.lis"],
                          "longest_palindrome_substring": ["palin.expand"], "max_product_subarray": ["greedy.kadane"],
                          "word_break": ["hash.set_lookup", "dp.prefix"]})
        for name in ("coin_change", "longest_increasing_subsequence", "palindromic_substrings", "partition_equal_subset"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_24(self):
        self.assert_audited("24_dynamic_programming_2d")
        self.assert_teaches({"lcs_cell": ["dp.two_strings"], "min_path_sum": ["dp.grid"], "stock_cooldown": ["dp.states"],
                             "matrix_chain": ["dp.interval"]})
        self.assert_uses({"burst_balloons": ["dp.interval"], "target_sum": ["dp.knapsack01"], "coin_change_ii": ["dp.amounts"],
                          "longest_increasing_path": ["recursion.memo", "grid.neighbors"], "diff_lines": ["bfs.path", "dp.two_strings"]})
        for name in ("stock_cooldown", "matrix_chain"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_25(self):
        self.assert_audited("25_bit_tricks")
        self.assert_teaches({"get_bit": ["bits.shift_mask"], "hamming_weight": ["bits.clear_lowest"],
                             "single_number": ["bits.xor_cancel"], "cheapest_team": ["dp.bitmask"]})
        self.assert_uses({"min_xor_sum": ["bits.shift_mask", "dp.bitmask"], "is_power_of_two": ["bits.clear_lowest"],
                          "max_xor_pair": ["hash.complement", "bits.shift_mask", "bits.xor_cancel"],
                          "count_bits": ["dp.recurrence", "bits.shift_mask"]})
        self.assertEqual(self.problems["cheapest_team"]["difficulty"], "easy")

    def test_every_stage_4_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_4:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("groups_after_each", lambda a, w: a[0] >= 100_000 and len(a[1]) >= 100_000)       # BFS per edge
        big("subsets_ii", lambda a, w: len(a[0]) >= 24 and len(w) <= 200)                     # all 2^n, then dedupe
        big("coin_change", lambda a, w: a[1] >= 5_000)                                         # plain recursion
        big("coin_change", lambda a, w: a[1] >= 4_000 and w == -1)                             # backtracking with a prune
        big("longest_increasing_subsequence", lambda a, w: len(a[0]) >= 100_000)               # O(n²) DP
        big("palindromic_substrings", lambda a, w: len(a[0]) >= 100_000)                       # every substring
        big("partition_equal_subset", lambda a, w: len(a[0]) >= 100)                           # every subset
        big("partition_equal_subset", lambda a, w: len(a[0]) >= 40 and w is False)             # DFS with a prune
        big("partition_equal_subset", lambda a, w: a == ([3, 3, 2, 2, 2, 2],) and w is True)   # largest-first greedy
        big("stock_cooldown", lambda a, w: len(a[0]) >= 100_000)                               # plain recursion
        big("matrix_chain", lambda a, w: len(a[0]) >= 150)                                     # every bracketing
        big("cheapest_team", lambda a, w: len(a[0]) >= 60)                                     # every team
        big("cheapest_team", lambda a, w: len(a[0]) >= 120 and max(a[1]) - min(a[1]) <= 10)    # backtracking with a prune
        big("bellman_ford", lambda a, w: a[0] >= 300 and len(a[1]) >= 3_000)


STAGE_5 = ("26_range_queries", "27_string_matching", "28_advanced_dynamic_programming", "29_advanced_graphs")


class Stage5Audit(AuditBase):
    """Part 2, Stage 5: topics 26-29 fully audited (docs/superpowers/plans/2026-10-21-technique-coverage-stage-5.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        self.assertEqual(self.problems["count_inversions"]["topic_id"], "10_sorting_and_intervals")

    def test_merge_sort_is_taught_before_sort_list(self):
        self.assert_teaches({"count_inversions": ["sort.merge_count"]})
        self.assert_uses({"count_inversions": ["recursion.trust", "pointers.two_sequences"],
                          "sort_list": ["recursion.trust", "pointers.two_sequences", "sort.merge_count", "list.dummy",
                                        "list.fast_slow"]})
        self.assertEqual(self.problems["count_inversions"]["difficulty"], "easy")


    def test_topic_26(self):
        self.assert_audited("26_range_queries")
        self.assert_teaches({"fenwick_prefix": ["fenwick.prefix"], "num_array": ["fenwick.update"],
                             "range_max_updates": ["segtree.basic"], "rank_transform": ["array.rank_compress"]})
        self.assert_uses({"count_smaller": ["fenwick.prefix", "fenwick.update", "array.rank_compress"],
                          "falling_squares": ["segtree.basic", "array.rank_compress"], "reverse_pairs": ["sort.merge_count"],
                          "price_board": ["segtree.basic"], "num_matrix": ["prefix.sums"]})
        for name in ("range_max_updates", "rank_transform"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_27(self):
        self.assert_audited("27_string_matching")
        self.assert_teaches({"prefix_function": ["str.prefix_function"], "find_all": ["str.kmp"]})
        self.assert_uses({"shortest_palindrome": ["str.prefix_function"], "longest_happy_prefix": ["str.prefix_function"],
                          "longest_dup_substring": ["bsearch.first_true", "bsearch.on_answer"], "sum_of_scores": []})
        self.assertEqual(self.problems["longest_happy_prefix"]["difficulty"], "easy")


    def test_topic_28(self):
        self.assert_audited("28_advanced_dynamic_programming")
        self.assert_uses({"ones_and_zeroes": ["dp.knapsack01"], "stock_k_transactions": ["dp.states"],
                          "min_cost_cut_stick": ["dp.interval"], "partition_k_subsets": ["bits.shift_mask", "dp.bitmask"],
                          "stickers_to_spell": ["bfs.shortest", "bfs.implicit", "dp.bitmask"]})


    def test_topic_29(self):
        self.assert_audited("29_advanced_graphs")
        self.assert_teaches({"floyd_step": ["sp.floyd"], "has_negative_cycle": ["sp.negative_cycle"]})
        self.assert_uses({"city_fewest_reachable": ["sp.floyd"], "has_negative_cycle": ["sp.bellman_ford"],
                          "cracking_safe": ["graph.euler"], "critical_mst_edges": ["uf.find", "uf.union", "graph.mst"],
                          "find_arbitrage": ["bfs.path", "sp.bellman_ford", "sp.negative_cycle"]})
        self.assertEqual(self.problems["has_negative_cycle"]["difficulty"], "easy")

    def test_every_stage_5_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_5:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("count_inversions", lambda a, w: len(a[0]) >= 200_000)        # O(n²) pairs, or insort
        big("rank_transform", lambda a, w: len(a[0]) >= 100_000)          # count smaller values per number
        big("range_max_updates", lambda ops, w: len(ops) >= 60_000)       # max() over the range
        big("range_max_updates", lambda ops, w: sum(op[0] == "max_range" and op[2] - op[1] < 32 for op in ops) >= 10_000)
        big("has_negative_cycle", lambda a, w: a[0] >= 400 and len(a[1]) >= 4_000 and w is True)    # Floyd: O(n³)
        big("has_negative_cycle", lambda a, w: a[0] >= 400 and len(a[1]) >= 4_000 and w is False)

    def test_teacher_hints_stay_in_their_topic(self):
        # A teaching problem's hint must not send the learner to a later topic's technique.
        self.assertNotIn("Fenwick", self.problems["count_inversions"]["hint"])

    def test_kmp_explanation_covers_the_step_after_a_match(self):
        explain = server.parse_techniques(server.TECHNIQUES_FILE)["str.kmp"]["explain"]
        self.assertIn("after a match", explain)


STAGE_6 = ("30_number_theory", "31_geometry", "32_advanced_trees", "33_network_flow", "34_digit_dp_and_speedups")


class Stage6Audit(AuditBase):
    """Part 2, Stage 6: topics 30-34 fully audited (docs/superpowers/plans/2026-10-21-technique-coverage-stage-6.md)."""

    def test_topic_30(self):
        self.assert_audited("30_number_theory")
        self.assert_teaches({"mod_pow": ["nt.fast_pow"], "count_primes": ["nt.sieve"], "extended_gcd": ["nt.mod_inverse"],
                             "prime_factors": ["nt.trial_division"]})
        self.assert_uses({"binomials": ["nt.fast_pow", "nt.mod_inverse"], "euler_phi": ["nt.trial_division"],
                          "largest_factor_component": ["uf.find", "uf.union", "nt.trial_division"],
                          "factorize_all": ["nt.sieve"], "chinese_remainder": ["nt.mod_inverse"]})
        for name in ("extended_gcd", "prime_factors"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_31(self):
        self.assert_audited("31_geometry")
        self.assert_teaches({"orientation": ["geo.cross"], "convex_hull": ["geo.hull"], "polygon_area": ["geo.shoelace"]})
        self.assert_uses({"fence_planner": ["geo.cross", "geo.hull", "geo.shoelace"],
                          "rectangle_area_ii": ["intervals.merge", "intervals.sort_by_start"],
                          "max_points_on_line": ["hash.group_key"], "segments_intersect": ["geo.cross"]})


    def test_topic_32(self):
        self.assert_audited("32_advanced_trees")
        self.assert_teaches({"lift_jump": ["tree.lift_jump"], "tree_ancestor": ["tree.lift_table"],
                             "subtree_sizes": ["tree.bfs_order"], "lca_queries": ["tree.lca"],
                             "min_edge_reversals": ["tree.reroot"]})
        self.assert_uses({"sum_of_distances": ["tree.bfs_order", "tree.reroot"],
                          "path_weight_queries": ["prefix.sums", "tree.lift_table", "tree.lca"],
                          "family_tree": ["tree.lift_table", "tree.bfs_order", "tree.lca"]})
        for name in ("lca_queries", "min_edge_reversals"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_33(self):
        self.assert_audited("33_network_flow")
        self.assert_teaches({"max_flow": ["flow.augment"], "min_cut_edges": ["flow.min_cut"], "max_staffing": ["flow.model"]})
        self.assert_uses({"project_selection": ["flow.augment", "flow.min_cut", "flow.model"],
                          "min_cost_flow": ["sp.bellman_ford", "flow.augment"],
                          "schedule_interviews": ["flow.augment", "flow.model"]})
        for name in ("min_cut_edges", "max_staffing"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)


    def test_topic_34(self):
        self.assert_audited("34_digit_dp_and_speedups")
        self.assert_teaches({"digit_choices": ["dp.digit"], "count_without_digit": ["dp.digit_started"]})
        self.assert_uses({"count_stepping_numbers": ["recursion.memo", "prefix.sums", "dp.digit", "dp.digit_started"],
                          "constrained_subset_sum": ["greedy.kadane", "deque.monotonic", "dp.recurrence"],
                          "jump_game_vi": ["deque.monotonic", "dp.recurrence"], "count_digit_one": []})

    def test_every_stage_6_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_6:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("prime_factors", lambda a, w: a[0] >= 10**11 and len(w) == 1)          # every number up to n
        big("extended_gcd", lambda a, w: min(a) >= 10**15)                          # search for x
        big("lca_queries", lambda a, w: len(a[0]) >= 50_000 and len(a[1]) >= 50_000)    # walk up one by one
        big("min_edge_reversals", lambda a, w: a[0] >= 20_000)                      # BFS from every node
        big("subtree_sizes", lambda a, w: a[0] >= 100_000)                          # recursion: too deep

    def test_lca_big_tests_meet_far_above_both_nodes(self):
        # Lifting to equal depth, then stepping both nodes up one parent at a time, must time out:
        # the big test needs many queries whose answer is far above both nodes.
        def depths(parent):
            children = [[] for _ in parent]
            for v in range(1, len(parent)):
                children[parent[v]].append(v)
            depth, order = [0] * len(parent), [0]
            for v in order:
                for c in children[v]:
                    depth[c] = depth[v] + 1
                    order.append(c)
            return depth

        def far(depth, pairs):
            return sum(min(depth[u], depth[v]) - depth[c] >= 1_000 for u, v, c in pairs)

        best = 0
        for (parent, queries), want in self.cases_of("lca_queries"):
            best = max(best, far(depths(parent), [(u, v, c) for (u, v), c in zip(queries, want)]))
        self.assertGreaterEqual(best, 35_000, "lca_queries")
        best = 0
        for calls, want in self.cases_of("family_tree"):
            pairs = [(call[1], call[2], c) for call, c in zip(calls, want) if call[0] == "common_ancestor"]
            best = max(best, far(depths(calls[0][1]), pairs))
        self.assertGreaterEqual(best, 12_000, "family_tree")     # counts common_ancestor only; distance and relation climb too

    def test_max_staffing_tests_reject_greedy_seat_filling(self):
        # Solving max_staffing marks flow.model learned, so filling seats greedily must fail a test.
        def greedy(worker_key, project_key, tie):
            def solve(limit, need, can):
                opts = [sorted({j for i, j in can if i == w}) for w in range(len(limit))]
                cands = [sum(1 for i, j in set(can) if j == p) for p in range(len(need))]
                left, seats, total = list(limit), list(need), 0
                for w in sorted(range(len(limit)), key=lambda w: (worker_key(w, limit, opts), tie * w)):
                    for p in sorted(opts[w], key=lambda p: (project_key(p, seats, cands), tie * p)):
                        if left[w] and seats[p] > 0:
                            left[w], seats[p], total = left[w] - 1, seats[p] - 1, total + 1
                return total
            return solve

        workers = {"in order": lambda w, L, o: w, "fewest options": lambda w, L, o: len(o[w])}
        projects = {"in order": lambda p, s, c: p, "most seats left": lambda p, s, c: -s[p],
                    "fewest candidates": lambda p, s, c: c[p]}
        cases = self.cases_of("max_staffing")
        for wname, wkey in workers.items():
            for pname, pkey in projects.items():
                for tie in (1, -1):     # break ties by lowest index, then by highest
                    solve = greedy(wkey, pkey, tie)
                    self.assertTrue(any(solve(*args) != want for args, want in cases), (wname, pname, tie))


if __name__ == "__main__":
    unittest.main()
