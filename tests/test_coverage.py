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

    def test_unaudited_is_a_warning_only(self):
        c = course(("01_a", [("snip", "snippet", "", [], ["t.x", "t.y"]), ("old", "solo", "hard", [], [])]))
        c[1]["old"]["audited"] = False
        errors, warnings = run(c)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["old (01_a): not audited yet"])


class RealCourse(unittest.TestCase):
    def test_no_coverage_errors(self):
        topics, problems = server.load_course()
        errors, _ = check_coverage(topics, problems, server.parse_techniques(server.TECHNIQUES_FILE))
        self.assertEqual(errors, [])


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


class Stage1Audit(unittest.TestCase):
    """Part 2, Stage 1: topics 01-05 fully audited (docs/superpowers/plans/2026-10-16-technique-coverage-stage-1.md)."""

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

    def test_every_stage_1_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_1:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_tags_stay_out_of_starters(self):
        leaks = [n for n, p in self.problems.items() if "USES" in p["starter"] or "TEACHES" in p["starter"]]
        self.assertEqual(leaks, [])


if __name__ == "__main__":
    unittest.main()
