# Technique coverage, Part 2 Stage 4: audit topics 20–25 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in topics 20–25 lists the techniques it uses. Each of those techniques is
taught by a basic problem that comes earlier, and no Stage 4 problem relies on a later topic. Topic
19 was audited in Part 1.

**Architecture:** Content work only. 23 techniques join `course/techniques.py` (90 in all). Every
Stage 4 problem gets `USES` (and `TEACHES` on teachers), including the two problems Stage 3 moved
in: `word_search_ii` (22) and `concatenated_words` (23). Five new easy teachers are added, and seven
problems are re-ranked to easy. `largest_factor_component` moves to Number theory. A `Stage4Audit`
test class pins it all.

**Tech Stack:** Python 3.12 stdlib, `unittest`, `--check`, and the Node headless-Chrome scenarios.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`. The Stage 3 plan,
`docs/superpowers/plans/2026-10-20-technique-coverage-stage-3.md`, is the model; its Global
Constraints all still apply.

## Global Constraints

- No new dependencies. Names, topic ids and drill keys never change; files may move between topics.
- Tags go directly above `TESTS =`, after the function, class, `PREPARE`, `FINISH` and `CHECK`.
  `USES` is in teaching order (`test_uses_are_in_teaching_order` enforces it).
- One teacher per technique (a snippet, guided or easy problem), before every user. Nothing from a
  later topic. At least two hards per topic. Headers are 84 wide. Line endings are kept.
- A teacher's big test must time out (2 s, `runner/judge.py`) for the naive solution a learner
  without the technique would write. **Exceptions in this stage:**
  - `single_number` (XOR saves space, not time) and `hamming_weight` (a bit-by-bit loop is just as fast).
  - `mst_cost`: every way to solve it is a spanning-tree algorithm.
  - `euler_path`: the natural naive version, walking until stuck, is wrong rather than slow, and its tests catch it.
- Each new problem was run through the real judge on the bundled Python while this plan was written.
  The references pass, the naive versions time out or fail, and small cases agree with brute force.
- `TAG` is the Stage 2 helper: `C:/Users/sam/AppData/Local/Temp/claude/C--Users-sam-Desktop-dsa/37698c59-d18f-494f-9d0b-cad64d5356c4/scratchpad/s2/tag.py`.
- End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Audit results

**New techniques (23), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `uf.find` | Union-find: finding the root | `find_root` (snippet, 20) | reuse |
| `graph.topo_kahn` | Topological order (Kahn's algorithm) | `build_order` (guided, 20) | reuse |
| `uf.union` | Union-find: merging groups | `groups_after_each` | **new** easy in 20, which had none. `count_components` stays a medium: BFS also solves it, so it can't teach union-find |
| `sp.relax` | Relaxing an edge | `relax` (snippet, 21) | reuse |
| `sp.dijkstra` | Dijkstra's algorithm | `cheapest_path` (guided, 21) | reuse |
| `graph.mst` | Minimum spanning tree | `mst_cost` | **new** easy in 21: the spec's Prim gap (`min_cost_connect_points`); spanning trees come back in 29 |
| `graph.euler` | Using every edge once (Hierholzer) | `euler_path` | **new** easy in 21: the spec's gap (`reconstruct_itinerary`); comes back in 29 (`cracking_safe`) |
| `bt.core` | Backtracking: choose, explore, un-choose | `combinations` (guided, 22) | reuse |
| `bt.skip_duplicates` | Skipping duplicate branches | `subsets_ii` | **re-rank** medium → easy; `combination_sum_ii` relies on it. `subsets` becomes easy too, so it comes first |
| `dp.recurrence` | Building answers from smaller ones | `robber_step` (snippet, 23) | reuse |
| `dp.prefix` | DP over prefixes | `decode_ways` (guided, 23) | reuse; `word_break`, `concatenated_words` and `decode_ways_ii` rely on it |
| `dp.amounts` | DP over amounts | `coin_change` | **re-rank** medium → easy; `combination_sum_iv` and `coin_change_ii` rely on it |
| `dp.lis` | Longest increasing subsequence with tails | `longest_increasing_subsequence` | **re-rank** medium → easy, with a 100,000-number test; `russian_doll` relies on it |
| `palin.expand` | Expanding around a centre | `palindromic_substrings` | **re-rank** medium → easy, with a 100,000-letter test; `longest_palindrome_substring` relies on it |
| `dp.knapsack01` | 0/1 knapsack: reachable sums | `partition_equal_subset` | **re-rank** medium → easy; `knapsack` and `target_sum` (24), and later `ones_and_zeroes` (28), rely on it |
| `dp.two_strings` | A table over two prefixes | `lcs_cell` (snippet, 24) | reuse |
| `dp.grid` | DP on a grid | `min_path_sum` (guided, 24) | reuse |
| `dp.states` | A few states per step | `stock_cooldown` | **re-rank** medium → easy, with a 100,000-day test; `stock_k_transactions` (28) relies on it |
| `dp.interval` | DP over intervals | `matrix_chain` | **new** easy in 24: the spec's interval-DP gap (`burst_balloons`); comes back in 28 (`min_cost_cut_stick`) |
| `bits.shift_mask` | Shifts and masks | `get_bit` (snippet, 25) | reuse |
| `bits.clear_lowest` | Clearing the lowest set bit | `hamming_weight` (easy, 25) | reuse |
| `bits.xor_cancel` | XOR cancels pairs | `single_number` (easy, 25) | reuse |
| `dp.bitmask` | DP over subsets as bitmasks | `cheapest_team` | **new** easy in 25: the spec's bitmask-DP gap (`min_xor_sum`); comes back in 28 |

**Spec gaps kept as a hard's own insight**, because they don't come back anywhere in the course
(checked with grep):
- `swim_rising_water`: a route costs its highest cell.
- `cherry_pickup_ii`: both robots in one state.
- `dungeon_game`: DP run backwards from the goal.
- `max_xor_pair`: the answer built bit by bit.

`min_cost_in_time`'s reference is Dijkstra over (cost, time, city) states, so it needs `bfs.state`
(19) and `sp.dijkstra`, both taught earlier. `longest_increasing_path` is memoisation (05) on grid
neighbours (19).

**Moved:** `largest_factor_component` (20) → `30_number_theory`. It needs prime factorisation by
trial division, which the spec places in topic 30. Stage 6 tags it there. Topic 20 keeps two hards
(`alien_dictionary`, `parallel_courses_iii`).

**Tags for every problem.** USES is in teaching order.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 20 | `find_root` (snippet) | `uf.find` | | |
| 20 | `build_order` (guided) | `graph.topo_kahn` | `graph.adjacency` | |
| 20 | `groups_after_each` (new) | `uf.union` | `uf.find` | |
| 20 | `course_schedule` | | `graph.adjacency`, `graph.topo_kahn` | |
| 20 | `graph_valid_tree`, `count_components`, `redundant_connection`, `network` (build) | | `uf.find`, `uf.union` | own: n − 1 edges; the first edge inside one group; union by size |
| 20 | `alien_dictionary`, `parallel_courses_iii` (hard) | | `graph.adjacency`, `graph.topo_kahn` | own: the first difference gives a rule; finish = time + latest prerequisite |
| 21 | `relax` (snippet) | `sp.relax` | | |
| 21 | `cheapest_path` (guided) | `sp.dijkstra` | `heap.lazy_delete`, `graph.adjacency`, `sp.relax` | |
| 21 | `mst_cost` (new) | `graph.mst` | `uf.find`, `uf.union` | |
| 21 | `euler_path` (new) | `graph.euler` | `graph.adjacency` | |
| 21 | `cheapest_flights` | | `sp.relax` | own: k rounds, each reading a copy |
| 21 | `min_cost_connect_points` | | `heap.lazy_delete`, `graph.mst` | own: every pair is an edge |
| 21 | `network_delay` | | `sp.dijkstra` | own: the answer is the largest distance |
| 21 | `min_cost_in_time` (hard) | | `bfs.state`, `sp.dijkstra` | own: keep a state only if it's faster than every cheaper one |
| 21 | `min_weighted_subgraph` (hard) | | `flood.from_targets`, `sp.dijkstra` | own: the Y shape |
| 21 | `reconstruct_itinerary` (hard) | | `graph.euler` | own: sorted destinations give the smallest trip |
| 21 | `swim_rising_water` (hard) | | `grid.neighbors`, `sp.dijkstra` | own: a route costs its highest cell |
| 21 | `route_planner` (build) | | `bfs.path`, `sp.dijkstra` | |
| 22 | `is_safe` (snippet) | | | |
| 22 | `combinations` (guided) | `bt.core` | `recursion.trust` | |
| 22 | `subsets` (now easy), `letter_combinations`, `permutations`, `palindrome_partition`, `combination_sum`, `expression_add_operators` (hard) | | `bt.core` | own: used flags; palindromic pieces; reuse by recursing with i; undo the last term for * |
| 22 | `subsets_ii` (now easy) | `bt.skip_duplicates` | `bt.core` | |
| 22 | `combination_sum_ii` | | `bt.core`, `bt.skip_duplicates` | |
| 22 | `generate_parentheses`, `remove_invalid_parentheses` (hard) | | `brackets.balance`, `bt.core` | own: count the removals first |
| 22 | `word_search` | | `grid.neighbors`, `bt.core` | own: mark and unmark the cell |
| 22 | `n_queens` (hard) | | `hash.group_key`, `bt.core` | own: column and diagonal sets |
| 22 | `word_search_ii` (hard, moved in) | | `trie.walk`, `grid.neighbors`, `bt.core` | own: walk the trie while searching |
| 22 | `solve_sudoku` (build) | | `hash.set_lookup`, `bt.core` | own: fewest options first |
| 23 | `robber_step` (snippet) | `dp.recurrence` | | |
| 23 | `decode_ways` (guided) | `dp.prefix` | `dp.recurrence` | |
| 23 | `climb_stairs` | | `recursion.memo`, `dp.recurrence` | |
| 23 | `min_cost_stairs`, `house_robber` | | `dp.recurrence` | |
| 23 | `coin_change` (now easy) | `dp.amounts` | `dp.recurrence` | |
| 23 | `longest_increasing_subsequence` (now easy) | `dp.lis` | `bsearch.first_true` | |
| 23 | `palindromic_substrings` (now easy) | `palin.expand` | | |
| 23 | `partition_equal_subset` (now easy) | `dp.knapsack01` | | |
| 23 | `combination_sum_iv` | | `dp.amounts` | own: amounts outside counts orders |
| 23 | `house_robber_ii` | | `dp.recurrence` | own: run it twice, leaving out each end |
| 23 | `longest_palindrome_substring` | | `palin.expand` | |
| 23 | `max_product_subarray` | | `greedy.kadane` | own: track the smallest too |
| 23 | `word_break` | | `hash.set_lookup`, `dp.prefix` | own: try every last word |
| 23 | `concatenated_words` (hard, moved in) | | `trie.walk`, `dp.prefix` | own: walk the trie for the last pieces, at least two |
| 23 | `decode_ways_ii` (hard) | | `dp.prefix` | own: count what a starred group can be |
| 23 | `frog_jump` (hard) | | `hash.set_lookup`, `dp.recurrence` | own: the state includes the last jump |
| 23 | `russian_doll` (hard) | | `dp.lis` | own: widths up, heights down on ties |
| 23 | `travel_passes` (build) | | `bfs.path`, `dp.recurrence` | |
| 24 | `lcs_cell` (snippet) | `dp.two_strings` | | |
| 24 | `min_path_sum` (guided) | `dp.grid` | | |
| 24 | `stock_cooldown` (now easy) | `dp.states` | | |
| 24 | `matrix_chain` (new) | `dp.interval` | | |
| 24 | `knapsack`, `target_sum` | | `dp.knapsack01` | own: values instead of yes/no; carry counts for + and − |
| 24 | `coin_change_ii` | | `dp.amounts` | own: coins outside counts combinations |
| 24 | `interleaving_string`, `longest_common_subsequence`, `distinct_subsequences` (hard), `edit_distance` (hard), `regex_matching` (hard) | | `dp.two_strings` | own: index i + j in s3; count ways; three edits; the star |
| 24 | `unique_paths` | | `dp.grid` | |
| 24 | `burst_balloons` (hard) | | `dp.interval` | own: the last balloon in an interval |
| 24 | `cherry_pickup_ii`, `dungeon_game` (hard) | | `dp.grid` | own: both robots in one state; backwards from the goal |
| 24 | `longest_increasing_path` (hard) | | `recursion.memo`, `grid.neighbors` | own: values only rise, so there are no cycles |
| 24 | `diff_lines` (build) | | `bfs.path`, `dp.two_strings` | |
| 25 | `get_bit` (snippet) | `bits.shift_mask` | | |
| 25 | `reverse_bits` (guided), `total_hamming_distance` (hard), `permissions` (build) | | `bits.shift_mask` | own: count each bit position on its own |
| 25 | `count_bits` | | `dp.recurrence`, `bits.shift_mask` | |
| 25 | `hamming_weight` | `bits.clear_lowest` | | |
| 25 | `is_power_of_two` | | `bits.clear_lowest` | |
| 25 | `single_number` | `bits.xor_cancel` | | |
| 25 | `cheapest_team` (new) | `dp.bitmask` | `bits.shift_mask` | |
| 25 | `reverse_integer` | | | own: check the range at the end |
| 25 | `get_sum` | | `bits.shift_mask`, `bits.xor_cancel` | own: AND then shift is the carry |
| 25 | `max_xor_pair` (hard) | | `hash.complement`, `bits.shift_mask`, `bits.xor_cancel` | own: decide the answer's bits from the top |
| 25 | `min_xor_sum` (hard) | | `bits.shift_mask`, `dp.bitmask` | own: the popcount says which a comes next |

## Review Focus

1. **Moved problems keep their history.** `largest_factor_component` keeps its progress and study-plan
   entries. Owners: `test_problems_moved_to_the_topic_of_their_last_prerequisite` and
   `test_every_plan_item_exists`.
2. **Teachers can't be passed by a shortcut.** The listed exceptions aside, the naive versions must
   time out. Owner: the Task 7 test `test_teacher_big_tests_reject_the_naive_solution`, plus the
   judge runs listed under Global Constraints.
3. **A wrong Euler route fails.** `euler_path`'s `CHECK` accepts any route that starts at 0 and uses
   each road exactly once, and nothing else. Owner: `--check euler_path`, plus its tests where walking
   until stuck leaves roads unused.
4. **Re-ranking and moving keep two hards in every topic.** Owner: the Task 7 test
   `test_every_stage_4_topic_keeps_two_hard_problems`.
5. **Hints don't point forward.** A teacher's hint must not send the learner to a later problem:
   `subsets_ii` loses "like Combination Sum II", and `palindromic_substrings` loses its pointer to
   Longest Palindromic Substring. Owner: Tasks 4 and 5, checked by reading the diff.

---

### Task 1: The move and the test class

**Files:** `tests/test_coverage.py`; move `course/4_advanced/20_topological_sort_and_union_find/largest_factor_component.py` →
`course/6_specialist_topics/30_number_theory/`; the spec.

- [ ] **Step 1: Failing test** above `if __name__ == "__main__":`:

```python
STAGE_4 = ("20_topological_sort_and_union_find", "21_weighted_graphs", "22_backtracking",
           "23_dynamic_programming_1d", "24_dynamic_programming_2d", "25_bit_tricks")


class Stage4Audit(AuditBase):
    """Part 2, Stage 4: topics 20-25 fully audited (docs/superpowers/plans/2026-10-21-technique-coverage-stage-4.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        self.assertEqual(self.problems["largest_factor_component"]["topic_id"], "30_number_theory")
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected: it fails with
  `'20_topological_sort_and_union_find' != '30_number_theory'`.
- [ ] **Step 3: Move** the file with `git mv`. `grep -rn largest_factor_component web course/*/*/lesson.py` prints nothing.
- [ ] **Step 4: Spec.** In the variants table:
  - Prim: ` (fixed: the new \`mst_cost\` teaches spanning trees)`.
  - Bottleneck: ` (kept as \`swim_rising_water\`'s own insight: it doesn't recur)`.
  - Euler: ` (fixed: the new \`euler_path\` teaches it)`.
  - DP over (time, node): ` (fixed: the reference is Dijkstra over (cost, time, city) states, taught by \`bfs.state\` and \`cheapest_path\`)`.
  - Interval DP: ` (fixed: the new \`matrix_chain\` teaches it)`.
  - Two walkers: ` (kept as \`cherry_pickup_ii\`'s own insight)`.
  - DP backwards: ` (kept as \`dungeon_game\`'s own insight)`.
  - Memoised grid DFS: ` (fixed: memoisation (05) and grid neighbours (19) cover it)`.
  - Bitmask DP: ` (fixed: the new \`cheapest_team\` teaches it)`.
  - Bit by bit: ` (kept as \`max_xor_pair\`'s own insight)`.

  In the later-topic table, the `largest_factor_component` (20) row gets ` (fixed: moved there)`.
- [ ] **Step 5: Run** the unit tests (all pass) and `python server.py --check largest_factor_component coverage`:
  one `ok` under topic 30; `67 techniques, 168 problem(s) not audited yet`; `All good.`
- [ ] **Step 6: Commit** `Stage 4 audit setup: largest_factor_component moved to Number theory`.

### Task 2: Topic 20, topological sort and union-find

- [ ] **Step 1: Failing test:**

```python
    def test_topic_20(self):
        self.assert_audited("20_topological_sort_and_union_find")
        self.assert_teaches({"find_root": ["uf.find"], "build_order": ["graph.topo_kahn"], "groups_after_each": ["uf.union"]})
        self.assert_uses({"course_schedule": ["graph.adjacency", "graph.topo_kahn"],
                          "redundant_connection": ["uf.find", "uf.union"], "network": ["uf.find", "uf.union"],
                          "parallel_courses_iii": ["graph.adjacency", "graph.topo_kahn"]})
        self.assertEqual(self.problems["groups_after_each"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** it: `test_topic_20` fails.
- [ ] **Step 3: Registry** (above `    "grid.neighbors": {`):

```python
    "uf.find": {
        "name": "Union-find: finding the root",
        "explain": "Union-find keeps groups as trees in a `parent` list: `parent[x] == x` means x is the root, the "
                   "group's name. To find x's group, follow parents up to the root. On the way, point the nodes you "
                   "passed straight at the root (path compression), so later finds are nearly instant.",
    },
    "graph.topo_kahn": {
        "name": "Topological order (Kahn's algorithm)",
        "explain": "To order tasks so every prerequisite comes first, count each task's unfinished prerequisites. "
                   "Start a queue with the tasks that have none. Pop one, add it to the order, and take 1 off each "
                   "task that waits on it, queueing any that reach 0. Tasks never reached are stuck in a cycle.",
    },
    "uf.union": {
        "name": "Union-find: merging groups",
        "explain": "To join the groups of a and b, find both roots. If they're the same, a and b were already "
                   "connected, so this link closes a cycle. Otherwise point one root at the other: two groups became "
                   "one. Counting the merges tells you how many groups are left.",
    },
```

- [ ] **Step 4: New teacher** `course/4_advanced/20_topological_sort_and_union_find/groups_after_each.py`:

```python
"""
Groups After Each Friendship                                                  [easy]

n people (0 to n - 1) start as strangers, each in a group of their own. The
friendships in `edges` form one at a time, and friends of friends end up in
the same group. Return the number of groups after each friendship.

Example:
    groups_after_each(4, [[0, 1], [2, 3], [1, 0], [1, 2]])  ->  [3, 2, 2, 1]
        [1, 0] joins two people already in one group, so nothing changes.

Aim for:  about O(n + edges). The last test has 100,000 people and 100,000
          friendships: counting the groups again with BFS after each one times out.
Hint:     Union-find. Keep parent (everyone starts as their own root) and a count of
          groups. For a friendship (a, b), find both roots. If they differ, point
          one root at the other: two groups became one, so subtract 1.
"""


def groups_after_each(n: int, edges: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _fast(n, edges):
    parent, groups, out = list(range(n)), n, []
    for a, b in edges:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        if a != b:
            parent[a] = b
            groups -= 1
        out.append(groups)
    return out


def _big():
    import random
    rng = random.Random(2001)
    edges = [[rng.randrange(100_000), rng.randrange(100_000)] for _ in range(100_000)]
    return (100_000, edges), _fast(100_000, edges)


TEACHES = ["uf.union"]
USES = ["uf.find"]

TESTS = [
    ((4, [[0, 1], [2, 3], [1, 0], [1, 2]]), [3, 2, 2, 1]),
    ((1, []), []),
    ((3, [[0, 0]]), [3]),
    ((5, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 0]]), [4, 3, 3, 2, 1]),
    ((6, [[5, 4], [3, 2], [1, 0], [4, 2], [0, 3]]), [5, 4, 3, 2, 1]),
    _big(),
]
```

  `solutions/groups_after_each.py`:

```python
def groups_after_each(n: int, edges: list[list[int]]) -> list[int]:
    # Union-find: a friendship between two different roots merges two groups into one.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving keeps the trees shallow
            x = parent[x]
        return x

    groups, out = n, []
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
        out.append(groups)
    return out
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/4_advanced/20_topological_sort_and_union_find find_root=:uf.find build_order=graph.adjacency:graph.topo_kahn course_schedule=graph.adjacency,graph.topo_kahn graph_valid_tree=uf.find,uf.union count_components=uf.find,uf.union redundant_connection=uf.find,uf.union alien_dictionary=graph.adjacency,graph.topo_kahn parallel_courses_iii=graph.adjacency,graph.topo_kahn network=uf.find,uf.union
```

- [ ] **Step 6: Run** the unit tests and `--check 20_ coverage`: 10 `ok`; `70 techniques, 159 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 4 audit: topic 20 tagged, with groups_after_each`.

### Task 3: Topic 21, weighted graphs

- [ ] **Step 1: Failing test:**

```python
    def test_topic_21(self):
        self.assert_audited("21_weighted_graphs")
        self.assert_teaches({"relax": ["sp.relax"], "cheapest_path": ["sp.dijkstra"], "mst_cost": ["graph.mst"],
                             "euler_path": ["graph.euler"]})
        self.assert_uses({"min_cost_connect_points": ["heap.lazy_delete", "graph.mst"],
                          "reconstruct_itinerary": ["graph.euler"], "min_cost_in_time": ["bfs.state", "sp.dijkstra"],
                          "swim_rising_water": ["grid.neighbors", "sp.dijkstra"], "route_planner": ["bfs.path", "sp.dijkstra"]})
        for name in ("mst_cost", "euler_path"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it: `test_topic_21` fails.
- [ ] **Step 3: Registry:**

```python
    "sp.relax": {
        "name": "Relaxing an edge",
        "explain": "Keep `dist`, the best distance found so far to each node. For an edge u → v of weight w, if "
                   "`dist[u] + w` beats `dist[v]`, update dist[v]. Every shortest-path algorithm is this one step, "
                   "repeated in a clever order.",
    },
    "sp.dijkstra": {
        "name": "Dijkstra's algorithm",
        "explain": "With no negative weights, pop the closest unsettled node from a min-heap of `(distance, node)`; "
                   "its distance is now final. Relax its edges, pushing every improvement. Skip a popped entry whose "
                   "distance is worse than the one already recorded: it's out of date.",
    },
    "graph.mst": {
        "name": "Minimum spanning tree",
        "explain": "To connect every node as cheaply as possible, take the cheapest edges first and skip any edge "
                   "that joins two nodes already connected (Kruskal: sort the edges, check with union-find). Prim "
                   "does the same from one node outward with a heap. Either way, n - 1 edges connect n nodes.",
    },
    "graph.euler": {
        "name": "Using every edge once (Hierholzer)",
        "explain": "To find a route that uses every edge exactly once, keep a stack. While the node on top has an "
                   "unused edge, take it and push where it leads. When it has none, pop it onto the route. Reverse "
                   "the route at the end. Loops you would get stuck in are spliced in automatically.",
    },
```

- [ ] **Step 4: New teachers.** `course/4_advanced/21_weighted_graphs/mst_cost.py`:

```python
"""
Connect Every City                                                            [easy]

Cities are 0 to n - 1. Each road [a, b, cost] could be built to join a and b
both ways. Return the smallest total cost of roads that connects every city to
every other (directly or through others), or -1 if that's impossible.

Example:
    mst_cost(4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]])  ->  7
        roads 0-1, 1-2 and 2-3. The road 0-2 would only join cities that are already joined.

Aim for:  O(roads log roads).
Hint:     Kruskal: sort the roads by cost and walk through them with union-find. Build a
          road when its two cities are in different groups, and skip it when they're
          already joined. Every city is connected once you've built n - 1 roads.
"""


def mst_cost(n: int, roads: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(n, roads):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = built = 0
    for a, b, c in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += c
            built += 1
    return total if built == n - 1 else -1


def _big():
    import random
    rng = random.Random(2101)
    n = 20_000
    roads = [[i, rng.randrange(i), rng.randint(1, 10**6)] for i in range(1, n)]    # a tree: connected
    roads += [[rng.randrange(n), rng.randrange(n), rng.randint(1, 10**6)] for _ in range(80_000)]
    return (n, roads), _fast(n, roads)


TEACHES = ["graph.mst"]
USES = ["uf.find", "uf.union"]

TESTS = [
    ((4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]]), 7),
    ((1, []), 0),
    ((2, []), -1),
    ((3, [[0, 1, 5], [0, 1, 2], [1, 2, 3]]), 5),
    ((4, [[0, 1, 1], [2, 3, 1]]), -1),
    ((5, [[0, 1, 4], [0, 2, 4], [1, 2, 2], [2, 3, 3], [2, 4, 2], [3, 4, 3]]), 11),
    _big(),
]
```

  `solutions/mst_cost.py`:

```python
def mst_cost(n: int, roads: list[list[int]]) -> int:
    # Kruskal: cheapest roads first; a road that joins two different groups is always worth building.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = built = 0
    for a, b, cost in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra != rb:                        # joins two groups: build it
            parent[ra] = rb
            total += cost
            built += 1
    return total if built == n - 1 else -1  # a tree on n cities has n - 1 roads
```

  `course/4_advanced/21_weighted_graphs/euler_path.py`:

```python
"""
One Stroke Through Every Road                                                 [easy]

Places are numbered 0 to n - 1, and each road [a, b] is ONE-WAY from a to b.
There is a route that starts at place 0 and drives along every road exactly
once (it may pass through a place many times). Return one such route as the
list of places in order. Any valid route is accepted.

Example:
    euler_path(3, [[0, 1], [1, 2], [2, 1], [1, 0], [0, 2]])  ->  [0, 1, 2, 1, 0, 2]

Aim for:  O(n + roads). Walking until you're stuck isn't enough: you can get stuck
          with roads still unused (see the tests with loops off the main path).
Hint:     Hierholzer's algorithm. Keep a stack, starting with [0]. Look at the place on top:
          if it still has an unused road, take it and push where it leads. If it has none,
          pop it onto the route. The route comes out backwards, so reverse it at the end.
          Each loop you got stuck before is spliced in where it belongs.
"""


def euler_path(n: int, roads: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected, args):
    """Any route that starts at 0 and uses every road exactly once."""
    n, roads = args
    if not isinstance(got, list) or not got or got[0] != 0:
        return False
    from collections import Counter
    return Counter(zip(got, got[1:])) == Counter(map(tuple, roads))


def _fast(n, roads):
    out = [[] for _ in range(n)]
    for a, b in roads:
        out[a].append(b)
    route, stack = [], [0]
    while stack:
        if out[stack[-1]]:
            stack.append(out[stack[-1]].pop())
        else:
            route.append(stack.pop())
    return route[::-1]


def _big():
    import random
    rng = random.Random(2102)
    n = 2_000
    walk = [0] + [rng.randrange(n) for _ in range(60_000)]      # one long walk is always one stroke
    roads = [[a, b] for a, b in zip(walk, walk[1:])]
    rng.shuffle(roads)
    return (n, roads), _fast(n, roads)


TEACHES = ["graph.euler"]
USES = ["graph.adjacency"]

TESTS = [
    ((3, [[0, 1], [1, 2], [2, 1], [1, 0], [0, 2]]), [0, 1, 2, 1, 0, 2]),
    ((2, [[0, 1]]), [0, 1]),
    ((1, []), [0]),
    ((4, [[0, 1], [1, 0], [0, 2], [2, 3]]), [0, 1, 0, 2, 3]),
    ((5, [[0, 1], [1, 2], [2, 0], [0, 3], [3, 4], [4, 0]]), [0, 1, 2, 0, 3, 4, 0]),
    ((4, [[0, 1], [1, 3], [1, 2], [2, 1]]), [0, 1, 2, 1, 3]),
    _big(),
]
```

  `solutions/euler_path.py`:

```python
def euler_path(n: int, roads: list[list[int]]) -> list[int]:
    # Hierholzer: walk while you can; a place with no roads left is finished and joins the route.
    out = [[] for _ in range(n)]
    for a, b in roads:
        out[a].append(b)
    route, stack = [], [0]
    while stack:
        if out[stack[-1]]:
            stack.append(out[stack[-1]].pop())      # take an unused road
        else:
            route.append(stack.pop())               # stuck here: this place is done
    return route[::-1]
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/4_advanced/21_weighted_graphs relax=:sp.relax cheapest_path=heap.lazy_delete,graph.adjacency,sp.relax:sp.dijkstra cheapest_flights=sp.relax min_cost_connect_points=heap.lazy_delete,graph.mst network_delay=sp.dijkstra min_cost_in_time=bfs.state,sp.dijkstra min_weighted_subgraph=flood.from_targets,sp.dijkstra reconstruct_itinerary=graph.euler swim_rising_water=grid.neighbors,sp.dijkstra route_planner=bfs.path,sp.dijkstra
```

- [ ] **Step 6: Run** the unit tests and `--check 21_ coverage`: 12 `ok`; `74 techniques, 149 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 4 audit: topic 21 tagged, with mst_cost and euler_path`.

### Task 4: Topic 22, backtracking

- [ ] **Step 1: Failing test:**

```python
    def test_topic_22(self):
        self.assert_audited("22_backtracking")
        self.assert_teaches({"combinations": ["bt.core"], "subsets_ii": ["bt.skip_duplicates"]})
        self.assert_uses({"combination_sum_ii": ["bt.core", "bt.skip_duplicates"],
                          "word_search_ii": ["trie.walk", "grid.neighbors", "bt.core"],
                          "n_queens": ["hash.group_key", "bt.core"], "generate_parentheses": ["brackets.balance", "bt.core"]})
        for name in ("subsets", "subsets_ii"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it: `test_topic_22` fails.
- [ ] **Step 3: Registry:**

```python
    "bt.core": {
        "name": "Backtracking: choose, explore, un-choose",
        "explain": "Build a solution one choice at a time. At each step, loop over the choices: make one (append to "
                   "the path), recurse to fill in the rest, then undo it (pop) before trying the next. Record a "
                   "COPY of the path when it's complete, and stop early on branches that can't work.",
    },
    "bt.skip_duplicates": {
        "name": "Skipping duplicate branches",
        "explain": "When the input has repeated values, sort it first. In the loop at each depth, skip a value equal "
                   "to the one just tried at the SAME depth: `if i > start and nums[i] == nums[i - 1]: continue`. "
                   "The same value deeper down is still allowed, so no answer is lost and none is repeated.",
    },
```

- [ ] **Step 4: Ranks.**
  - `subsets.py` and `subsets_ii.py` headers become `[easy]`, 84 wide.
  - In `subsets_ii.py`, the hint's `the same depth, like Combination Sum II.` becomes `the same depth.`
  - Add to its `TESTS` the test `(([1] * 12 + [2] * 12,), sorted([1] * i + [2] * j for i in range(13) for j in range(13)))`.
    Building all 2^24 subsets and removing repeats times out.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/4_advanced/22_backtracking is_safe= combinations=recursion.trust:bt.core combination_sum=bt.core combination_sum_ii=bt.core,bt.skip_duplicates generate_parentheses=brackets.balance,bt.core letter_combinations=bt.core palindrome_partition=bt.core permutations=bt.core subsets=bt.core subsets_ii=bt.core:bt.skip_duplicates word_search=grid.neighbors,bt.core expression_add_operators=bt.core n_queens=hash.group_key,bt.core remove_invalid_parentheses=brackets.balance,bt.core word_search_ii=trie.walk,grid.neighbors,bt.core solve_sudoku=hash.set_lookup,bt.core
```

- [ ] **Step 6: Run** the unit tests and `--check 22_ coverage`: 16 `ok`; `76 techniques, 133 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 4 audit: topic 22 tagged`.

### Task 5: Topic 23, DP in one dimension

- [ ] **Step 1: Failing test:**

```python
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
```

- [ ] **Step 2: Run** it: `test_topic_23` fails.
- [ ] **Step 3: Registry:**

```python
    "dp.recurrence": {
        "name": "Building answers from smaller ones",
        "explain": "Write the answer for position i in terms of answers for smaller positions, like "
                   "`best[i] = max(best[i - 1], best[i - 2] + x)`. Fill them in from the smallest up, so each one is "
                   "ready when it's needed. If only the last two are ever used, two variables are enough.",
    },
    "dp.prefix": {
        "name": "DP over prefixes",
        "explain": "To count or check ways to build a string piece by piece, let `ways[i]` describe the first i "
                   "characters. Work it out from shorter prefixes by asking what the LAST piece could be: one digit, "
                   "two digits, a word ending at i. `ways[0]` is the empty start.",
    },
    "dp.amounts": {
        "name": "DP over amounts",
        "explain": "When you can use items again and again to make a total, let `best[x]` be the answer for the "
                   "amount x. Fill x from 0 upwards: `best[x]` comes from `best[x - c]` for each item c that fits, "
                   "plus one more c. Plain recursion recomputes the same amounts over and over.",
    },
    "dp.lis": {
        "name": "Longest increasing subsequence with tails",
        "explain": "Keep `tails`, where `tails[k]` is the smallest possible last value of an increasing subsequence "
                   "of length k + 1. It stays sorted, so for each x, binary search for the first tail >= x and "
                   "replace it with x, or append x if there's none. The answer is `len(tails)`: O(n log n).",
    },
    "palin.expand": {
        "name": "Expanding around a centre",
        "explain": "Every palindrome has a centre: a letter, or the gap between two letters, so a string of n letters "
                   "has 2n - 1 centres. From each centre, grow outwards while the letters on both ends match. Each "
                   "step that succeeds is one more palindrome.",
    },
    "dp.knapsack01": {
        "name": "0/1 knapsack: reachable sums",
        "explain": "To pick a subset that hits a total, keep which sums are reachable, starting with just 0. For each "
                   "item x, every reachable s makes s + x reachable too. In an array, loop s DOWNWARDS so x isn't "
                   "used twice in one round. It's O(items × total), not 2^items.",
    },
```

- [ ] **Step 4: Ranks and big tests.** Headers of `coin_change`, `longest_increasing_subsequence`, `palindromic_substrings`
  and `partition_equal_subset` become `[easy]`, 84 wide.
  - `longest_increasing_subsequence.py`:
    - Its `Aim for:` line becomes `Aim for:  O(n log n). The last test has 100,000 numbers: the O(n²) DP (try it first) times out.`
    - Add a `_big()` above `TESTS`: `random.Random(2301)`, 100,000 numbers in `1..10**9`, with the expected value from an
      in-file patience `_fast`.
    - Append `_big()` to `TESTS`.
  - `palindromic_substrings.py`:
    - Its hint becomes: `Every palindrome has a centre: a letter, or the gap between two letters. From each of the`
      / `2n - 1 centres, grow outwards while both ends match; every step that works is one more palindrome.`
    - Above it, add `Aim for:  O(n²) at worst, far less on most strings. The last test has 100,000 random letters:`
      / `          checking every substring times out.`
    - Add a `_big()`: `random.Random(2302)`, 100,000 letters from "ab", with the expected value from an in-file expand
      `_fast`. Append it to `TESTS`.
  - `coin_change` (amount 6249: plain recursion times out) and `partition_equal_subset` (`[100] * 100 + [50, 50]`:
    trying subsets times out) already have big enough tests.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/4_advanced/23_dynamic_programming_1d robber_step=:dp.recurrence decode_ways=dp.recurrence:dp.prefix climb_stairs=recursion.memo,dp.recurrence min_cost_stairs=dp.recurrence coin_change=dp.recurrence:dp.amounts combination_sum_iv=dp.amounts house_robber=dp.recurrence house_robber_ii=dp.recurrence longest_increasing_subsequence=bsearch.first_true:dp.lis longest_palindrome_substring=palin.expand max_product_subarray=greedy.kadane palindromic_substrings=:palin.expand partition_equal_subset=:dp.knapsack01 word_break=hash.set_lookup,dp.prefix concatenated_words=trie.walk,dp.prefix decode_ways_ii=dp.prefix frog_jump=hash.set_lookup,dp.recurrence russian_doll=dp.lis travel_passes=bfs.path,dp.recurrence
```

- [ ] **Step 6: Run** the unit tests and `--check 23_ coverage`: 19 `ok`; `82 techniques, 114 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 4 audit: topic 23 tagged`.

### Task 6: Topic 24, DP in two dimensions

- [ ] **Step 1: Failing test:**

```python
    def test_topic_24(self):
        self.assert_audited("24_dynamic_programming_2d")
        self.assert_teaches({"lcs_cell": ["dp.two_strings"], "min_path_sum": ["dp.grid"], "stock_cooldown": ["dp.states"],
                             "matrix_chain": ["dp.interval"]})
        self.assert_uses({"burst_balloons": ["dp.interval"], "target_sum": ["dp.knapsack01"], "coin_change_ii": ["dp.amounts"],
                          "longest_increasing_path": ["recursion.memo", "grid.neighbors"], "diff_lines": ["bfs.path", "dp.two_strings"]})
        for name in ("stock_cooldown", "matrix_chain"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it: `test_topic_24` fails.
- [ ] **Step 3: Registry:**

```python
    "dp.two_strings": {
        "name": "A table over two prefixes",
        "explain": "For two strings, let `dp[i][j]` be the answer for the first i letters of a and the first j of b. "
                   "If `a[i - 1] == b[j - 1]`, the two letters can pair up: build on `dp[i - 1][j - 1]`. Otherwise "
                   "drop a letter from one string: `dp[i - 1][j]` or `dp[i][j - 1]`.",
    },
    "dp.grid": {
        "name": "DP on a grid",
        "explain": "When you only move right or down, a cell's answer comes from the cell above and the cell to its "
                   "left. Fill the grid row by row. One row is enough: before you update `row[c]` it still holds "
                   "the cell above, and `row[c - 1]` is the cell to the left.",
    },
    "dp.states": {
        "name": "A few states per step",
        "explain": "When each step can leave you in one of a few situations (holding a share, just sold, resting), "
                   "keep the best total for each state. Every day, work out today's states from yesterday's, all "
                   "at once. It's O(n), with a handful of variables.",
    },
    "dp.interval": {
        "name": "DP over intervals",
        "explain": "When the answer for a run i..j depends on how it splits, let `cost[i][j]` be the answer for that "
                   "run and try every split point k: the parts i..k and k+1..j are shorter runs. So fill the table "
                   "by length, shortest runs first. It's usually O(n³).",
    },
```

- [ ] **Step 4: Ranks and big test.**
  - `stock_cooldown`'s header becomes `[easy]`, 84 wide.
  - Its `Aim for:` line becomes `Aim for:  O(n): a small state machine. The last test has 100,000 days.`
  - Add a `_big()`: `random.Random(2402)`, 100,000 prices in `0..10**4`, with the expected value from an in-file
    three-state `_fast`. Append it to `TESTS`.
- [ ] **Step 5: New teacher** `course/4_advanced/24_dynamic_programming_2d/matrix_chain.py`:

```python
"""
Matrix Chain Multiplication                                                   [easy]

Matrix i has dims[i] rows and dims[i + 1] columns, so there are len(dims) - 1
matrices to multiply in a row. Multiplying a p x q matrix by a q x r one costs
p * q * r. The order of the multiplications (where the brackets go) changes the
total cost. Return the smallest total cost.

Example:
    matrix_chain([10, 30, 5, 60])  ->  4500
        (A B) C costs 10*30*5 + 10*5*60 = 4500; A (B C) costs 30*5*60 + 10*30*60 = 27000.

Aim for:  O(n³) with n matrices. Trying every way of placing the brackets is
          exponential, and the last test has 150 matrices.
Hint:     cost[i][j] = cheapest way to multiply matrices i..j into one. The LAST
          multiplication splits them at some k: (i..k) times (k+1..j), which costs
          cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]. Fill
          the table for short runs first, then longer ones.
"""


def matrix_chain(dims: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(dims):
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = min(cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1] for k in range(i, j))
    return cost[0][n - 1]


def _big():
    import random
    rng = random.Random(2401)
    dims = [rng.randint(1, 100) for _ in range(151)]
    return (dims,), _fast(dims)


TEACHES = ["dp.interval"]
USES = []

TESTS = [
    (([10, 30, 5, 60],), 4500),
    (([40, 20, 30, 10, 30],), 26000),
    (([10, 20, 30],), 6000),
    (([5, 10],), 0),
    (([1, 2, 3, 4, 3],), 30),
    (([10, 20, 30, 40, 30],), 30000),
    _big(),
]
```

  `solutions/matrix_chain.py`:

```python
def matrix_chain(dims: list[int]) -> int:
    # Interval DP: the best way to multiply matrices i..j tries every place for the last split.
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]          # cost[i][j]: matrices i..j; one matrix costs 0
    for length in range(2, n + 1):              # shorter runs first, so the parts are ready
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = min(cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                             for k in range(i, j))
    return cost[0][n - 1]
```

- [ ] **Step 6: Tag.**

```bash
python $TAG course/4_advanced/24_dynamic_programming_2d lcs_cell=:dp.two_strings min_path_sum=:dp.grid knapsack=dp.knapsack01 stock_cooldown=:dp.states coin_change_ii=dp.amounts interleaving_string=dp.two_strings longest_common_subsequence=dp.two_strings target_sum=dp.knapsack01 unique_paths=dp.grid burst_balloons=dp.interval cherry_pickup_ii=dp.grid distinct_subsequences=dp.two_strings dungeon_game=dp.grid edit_distance=dp.two_strings longest_increasing_path=recursion.memo,grid.neighbors regex_matching=dp.two_strings diff_lines=bfs.path,dp.two_strings
```

- [ ] **Step 7: Run** the unit tests and `--check 24_ coverage`: 18 `ok`; `86 techniques, 97 problem(s) not audited yet`.
- [ ] **Step 8: Commit** `Stage 4 audit: topic 24 tagged, with matrix_chain`.

### Task 7: Topic 25, bit tricks

- [ ] **Step 1: Failing tests:**

```python
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
        big("longest_increasing_subsequence", lambda a, w: len(a[0]) >= 100_000)               # O(n²) DP
        big("palindromic_substrings", lambda a, w: len(a[0]) >= 100_000)                       # every substring
        big("partition_equal_subset", lambda a, w: len(a[0]) >= 100)                           # every subset
        big("stock_cooldown", lambda a, w: len(a[0]) >= 100_000)                               # plain recursion
        big("matrix_chain", lambda a, w: len(a[0]) >= 150)                                     # every bracketing
        big("cheapest_team", lambda a, w: len(a[0]) >= 60)                                     # every team
```

- [ ] **Step 2: Run** it: `test_topic_25` fails, and the big-test check fails on `cheapest_team`.
- [ ] **Step 3: Registry:**

```python
    "bits.shift_mask": {
        "name": "Shifts and masks",
        "explain": "Bit k of x is `(x >> k) & 1`. `1 << k` is a number with only bit k set: use `x | (1 << k)` to "
                   "set the bit, `x & ~(1 << k)` to clear it and `x & (1 << k)` to test it. A whole set of small "
                   "numbers fits in one int this way.",
    },
    "bits.clear_lowest": {
        "name": "Clearing the lowest set bit",
        "explain": "`n & (n - 1)` is n with its lowest 1 bit cleared, because subtracting 1 flips that bit and every "
                   "0 below it. Repeat it to visit only the set bits, or check `n & (n - 1) == 0` to see whether n "
                   "has exactly one bit set.",
    },
    "bits.xor_cancel": {
        "name": "XOR cancels pairs",
        "explain": "`x ^ x == 0` and `x ^ 0 == x`, and the order doesn't matter. So XOR-ing a list cancels every pair "
                   "and leaves whatever is unpaired. It also undoes itself: `a ^ b == c` exactly when `a ^ c == b`.",
    },
    "dp.bitmask": {
        "name": "DP over subsets as bitmasks",
        "explain": "When there are at most about 20 things, a set of them fits in an int: bit s is thing s. Then "
                   "`best[mask]` can be the answer for exactly that set, for all 2^n masks. Go through the masks in "
                   "increasing order, since adding a thing only adds bits: `best[mask | 1 << s]` builds on `best[mask]`.",
    },
```

- [ ] **Step 4: New teacher** `course/4_advanced/25_bit_tricks/cheapest_team.py`:

```python
"""
Cheapest Team for All Skills                                                  [easy]

There are k skills, numbered 0 to k - 1 (k is at most 12). Person i knows the
skills in people[i] and costs costs[i] to hire. Return the smallest total cost
of a team that, between them, knows every skill, or -1 if no team does.

Example:
    cheapest_team([[0], [1, 2], [0, 1], [2]], [4, 5, 3, 1], 3)  ->  4
        person 2 knows 0 and 1, person 3 knows 2: 3 + 1.

Aim for:  O(2^k * people). Trying every team is O(2^people), and the last test
          has 60 people.
Hint:     Write a set of skills as a bitmask: skill s is bit 1 << s. best[mask] = cheapest
          team that knows at least the skills in mask, starting with best[0] = 0. Go through
          the masks in increasing order, and for each person p, best[mask | p_mask] can be
          best[mask] + costs[p].
"""


def cheapest_team(people: list[list[int]], costs: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(people, costs, k):
    full, inf = (1 << k) - 1, float("inf")
    masks = [sum(1 << s for s in skills) for skills in people]
    best = [inf] * (1 << k)
    best[0] = 0
    for mask in range(1 << k):
        if best[mask] < inf:
            for m, c in zip(masks, costs):
                if best[mask] + c < best[mask | m]:
                    best[mask | m] = best[mask] + c
    return best[full] if best[full] < inf else -1


def _big():
    import random
    rng = random.Random(2501)
    people = [rng.sample(range(12), rng.randint(1, 3)) for _ in range(60)]
    costs = [rng.randint(1, 1000) for _ in range(60)]
    return (people, costs, 12), _fast(people, costs, 12)


TEACHES = ["dp.bitmask"]
USES = ["bits.shift_mask"]

TESTS = [
    (([[0], [1, 2], [0, 1], [2]], [4, 5, 3, 1], 3), 4),
    (([[0, 1, 2]], [7], 3), 7),
    (([[0], [1]], [1, 1], 3), -1),
    (([[0], [0], [1]], [5, 2, 3], 2), 5),
    (([[0, 1], [1, 2], [2, 3], [0, 3]], [3, 3, 3, 3], 4), 6),
    (([], [], 1), -1),
    _big(),
]
```

  `solutions/cheapest_team.py`:

```python
def cheapest_team(people: list[list[int]], costs: list[int], k: int) -> int:
    # Bitmask DP: best[mask] = cheapest team knowing the skills in mask. Hiring only adds bits,
    # so going through the masks in increasing order handles every team.
    full, inf = (1 << k) - 1, float("inf")
    masks = [sum(1 << s for s in skills) for skills in people]
    best = [inf] * (1 << k)
    best[0] = 0
    for mask in range(1 << k):
        if best[mask] == inf:
            continue
        for m, c in zip(masks, costs):
            if best[mask] + c < best[mask | m]:
                best[mask | m] = best[mask] + c
    return best[full] if best[full] < inf else -1
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/4_advanced/25_bit_tricks get_bit=:bits.shift_mask reverse_bits=bits.shift_mask count_bits=dp.recurrence,bits.shift_mask hamming_weight=:bits.clear_lowest is_power_of_two=bits.clear_lowest single_number=:bits.xor_cancel reverse_integer= get_sum=bits.shift_mask,bits.xor_cancel max_xor_pair=hash.complement,bits.shift_mask,bits.xor_cancel min_xor_sum=bits.shift_mask,dp.bitmask total_hamming_distance=bits.shift_mask permissions=bits.shift_mask
```

- [ ] **Step 6: Run** the unit tests (all pass) and `--check 25_ coverage`: 13 `ok`; `90 techniques, 85 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 4 audit: topic 25 tagged, with cheapest_team`.

### Task 8: README, browser check and full verification

- [ ] **Step 1:** README: `406 coding exercises` becomes `411 coding exercises`.
- [ ] **Step 2:** `tests/browser/stage_4.mjs`, with helpers and opening from `stage_3.mjs`. Checks:
  1. `#/t/23_dynamic_programming_1d`: the list equals `Building answers from smaller ones | DP over prefixes | DP over amounts | Longest increasing subsequence with tails | Expanding around a centre | 0/1 knapsack: reachable sums`.
  2. Solve `robber_step` and `decode_ways`.
  3. `#/p/coin_change`: `.tech-new h4` is `New technique: DP over amounts`.
  4. `#/p/combination_sum_iv`: `.reveal-box` includes `This uses DP over amounts` and `Coin Change teaches it`.
  5. Reset progress and placement; solve `lcs_cell` and `min_path_sum`; `#/p/target_sum`: `.tech-banner` includes
     `This uses 0/1 knapsack: reachable sums` and `Partition Equal Subset Sum`.
  6. No console errors. That is 9 checks.
- [ ] **Step 3:** In `tests/browser/README.md`, add `    bash tests/browser/fresh.sh 8174 stage_4.mjs` after the `stage_3.mjs` line.
- [ ] **Step 4: Run** it: 9 of 9. Then the earlier scenarios (23, 14, 15, 11) and Phase 1 (54).
- [ ] **Step 5:** Unit tests all pass. `python server.py --check`: 411 `ok`, `ok   starting check`, `90 techniques,
  85 problem(s) not audited yet`, `All good.`
- [ ] **Step 6: Commit** `Stage 4 audit: README count and a browser check for topic 23's techniques`.
