# Technique coverage, Part 2 Stage 5: audit topics 26–29 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in topics 26–29 lists the techniques it uses. Each of those techniques is
taught by a basic problem that comes earlier, and no Stage 5 problem relies on a later topic.

**Architecture:** Content work only. 8 techniques join `course/techniques.py` (99 in all). Every
Stage 5 problem gets `USES` (and `TEACHES` on teachers). Merge sort gets a teacher in topic 10,
before its first user (`sort_list`, 14): `count_inversions` moves there and becomes easy. Two new
easy teachers join topic 26, and `longest_happy_prefix` becomes easy. A `Stage5Audit` test class
pins it all.

**Tech Stack:** Python 3.12 stdlib, `unittest`, `--check`, the Node headless-Chrome scenarios, and
`runner/judge.py` on the bundled Python for shortcut timing.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`. The Stage 4 plan,
`docs/superpowers/plans/2026-10-21-technique-coverage-stage-4.md`, is the model; its Global
Constraints all still apply.

## Global Constraints

- No new dependencies. Names, topic ids and drill keys never change; files may move between topics.
- Tags go directly above `TESTS =`. `USES` is in teaching order (`test_uses_are_in_teaching_order` enforces it).
- One teacher per technique (a snippet, guided or easy problem), before every user. Nothing from a
  later topic. At least two hards per topic. Headers are 84 wide. Line endings are kept.
- A teacher's big test must time out (2 s) for the naive solution a learner without the technique
  would write. **Exception in this stage:** `range_max_updates`. Square-root blocks pass it as fast
  as a segment tree (538 ms against 440 ms in the judge), because `max()` over a slice runs at C
  speed. Square-root blocks are a valid range-query structure too.
- These were run through the real judge while this plan was written:
  - `count_inversions` at 200,000 numbers: the reference takes 0.95 s; `insort`, which passed at 100,000 (0.99 s), times out.
  - `rank_transform`: counting the smaller distinct values times out.
  - `range_max_updates`: `max()` over a slice times out.
- `TAG` is the Stage 2 helper: `C:/Users/sam/AppData/Local/Temp/claude/C--Users-sam-Desktop-dsa/37698c59-d18f-494f-9d0b-cad64d5356c4/scratchpad/s2/tag.py`.
- End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Audit results

**New techniques (8), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `sort.merge_count` | Merge sort, counting while merging | `count_inversions` | **move** 26 → `10_sorting_and_intervals` and **re-rank** medium → easy. Merge sort is `sort_list`'s insight (14), and it comes back in `reverse_pairs` (26), so its teacher must come before 14 |
| `fenwick.prefix` | Fenwick tree: prefix sums | `fenwick_prefix` (snippet, 26) | reuse |
| `fenwick.update` | Fenwick tree: updates | `num_array` (guided, 26) | reuse |
| `segtree.basic` | Segment tree | `range_max_updates` | **new** easy in 26: `price_board`, `falling_squares` and later `rectangle_area_ii` (31) rely on it |
| `array.rank_compress` | Compressing values to ranks | `rank_transform` | **new** easy in 26: `count_smaller`, `falling_squares` and `rectangle_area_ii` (31) rely on it |
| `str.prefix_function` | The prefix function | `prefix_function` (snippet, 27) | reuse |
| `str.kmp` | Matching with the prefix function (KMP) | `find_all` (guided, 27) | reuse |
| `sp.floyd` | Floyd–Warshall | `floyd_step` (snippet, 29) | reuse |

**Kept as a hard's own insight**, because grep shows none comes back later in the course:
- `range_min_queries`: the sparse table.
- `longest_dup_substring`: the rolling hash.
- `sum_of_scores`: the Z-function.
- `critical_connections`: low-link values.
- `count_scc`: Kosaraju.
- `min_obstacles`: 0-1 BFS.
- `is_bipartite`: two-colouring. Topic 33's bipartite matching is a different idea.

Topic 28 needs no new technique: each problem builds on DP shapes taught in 23–25.

**Other rank change:** `longest_happy_prefix` (27) becomes easy. It is exactly the last value of
the prefix function, so it has no insight of its own for a hard. Topic 27 keeps three hards.

**Tags for every problem.** USES is in teaching order.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 10 | `count_inversions` (moved, now easy) | `sort.merge_count` | `recursion.trust`, `pointers.two_sequences` | |
| 14 | `sort_list` | | adds `sort.merge_count` between `pointers.two_sequences` and `list.dummy` | |
| 26 | `fenwick_prefix` (snippet) | `fenwick.prefix` | `bits.clear_lowest` | |
| 26 | `num_array` (guided) | `fenwick.update` | `fenwick.prefix` | |
| 26 | `range_max_updates` (new) | `segtree.basic` | | |
| 26 | `rank_transform` (new) | `array.rank_compress` | | |
| 26 | `range_min_queries` | | | own: the sparse table |
| 26 | `num_matrix` | | `prefix.sums` | own: 2D inclusion-exclusion |
| 26 | `count_smaller` (hard) | | `fenwick.prefix`, `fenwick.update`, `array.rank_compress` | |
| 26 | `falling_squares` (hard) | | `segtree.basic`, `array.rank_compress` | own: lazily set a whole range |
| 26 | `reverse_pairs` (hard) | | `sort.merge_count` | own: count with two pointers before merging |
| 26 | `price_board` (build) | | `segtree.basic` | own: (sum, max, index) per node |
| 27 | `prefix_function` (snippet) | `str.prefix_function` | | |
| 27 | `find_all` (guided) | `str.kmp` | `str.prefix_function` | |
| 27 | `repeated_substring_pattern`, `longest_happy_prefix` (now easy) | | `str.prefix_function` | own: the period n − pi[-1] |
| 27 | `repeated_dna` | | `hash.seen_set`, `window.fixed`, `bits.shift_mask` | own: a 2-bit code per letter |
| 27 | `longest_dup_substring` (hard) | | `bsearch.first_true`, `bsearch.on_answer` | own: the rolling hash |
| 27 | `shortest_palindrome` (hard) | | `str.prefix_function` | own: s + "#" + reversed s |
| 27 | `sum_of_scores` (hard) | | | own: the Z-function |
| 27 | `shared_phrases` (build) | | `hash.set_lookup`, `window.fixed` | |
| 28 | `subset_sums` (snippet) | | `bits.clear_lowest`, `dp.bitmask` | |
| 28 | `shortest_tour` (guided), `partition_k_subsets` | | `bits.shift_mask`, `dp.bitmask` | own: the (mask, last) state; fill rolls over |
| 28 | `house_robber_iii` | | `tree.recursion`, `dp.states` | |
| 28 | `ones_and_zeroes` | | `dp.knapsack01` | own: two capacities |
| 28 | `stock_k_transactions` (hard) | | `dp.states` | own: k layers |
| 28 | `min_cost_cut_stick` (hard) | | `dp.interval` | own: add the ends |
| 28 | `min_palindrome_cuts` (hard) | | `dp.prefix`, `dp.interval` | |
| 28 | `stickers_to_spell` (hard) | | `bfs.shortest`, `bfs.implicit`, `dp.bitmask` | own: only stickers with the first uncovered letter |
| 28 | `best_job_schedule` (build) | | `bsearch.first_true`, `bfs.path`, `dp.recurrence` | |
| 29 | `floyd_step` (snippet) | `sp.floyd` | | |
| 29 | `city_fewest_reachable` (guided) | | `sp.floyd` | |
| 29 | `is_bipartite` | | `graph.components` | own: opposite colours |
| 29 | `has_negative_cycle` | | `sp.bellman_ford` | own: start everything at 0, one more round |
| 29 | `cracking_safe` (hard) | | `graph.euler` | own: (n − 1)-digit nodes |
| 29 | `critical_mst_edges` (hard) | | `uf.find`, `uf.union`, `graph.mst` | own: skip or force each edge |
| 29 | `critical_connections`, `count_scc` (hard) | | `graph.adjacency` | own: low-link; Kosaraju |
| 29 | `min_obstacles` (hard) | | `grid.neighbors` | own: 0-1 BFS |
| 29 | `find_arbitrage` (build) | | `bfs.path`, `sp.bellman_ford` | own: weights −log(rate) |

## Review Focus

1. **The moved teacher keeps its history and lands before its users.** `count_inversions` keeps its
   progress and plan entries, and topic 10 comes before 14 (`sort_list`) and 26 (`reverse_pairs`).
   Owners: `test_problems_moved_to_the_topic_of_their_last_prerequisite`,
   `test_every_plan_item_exists`, and the coverage check.
2. **Teachers can't be passed by a shortcut**, apart from the listed exception. Owner: the Task 5
   test `test_teacher_big_tests_reject_the_naive_solution`, plus the judge runs under Global Constraints.
3. **Class teachers behave like the rest.** `range_max_updates` uses the `CLASS` op format. Owner:
   `--check range_max_updates`.
4. **Two hards per topic.** Owner: the Task 5 test `test_every_stage_5_topic_keeps_two_hard_problems`.
5. **Topic 10's earlier audit still holds** after it gains an easy: `test_topic_10` (Stage 2) and
   the two-hards test for Stage 2. Owner: the unit suite in Task 1.

---

### Task 1: A merge-sort teacher in topic 10

**Files:** move `course/5_advanced_techniques/26_range_queries/count_inversions.py` → `course/2_core_patterns/10_sorting_and_intervals/`;
re-rank it; enlarge its big test; `course/techniques.py`; `14_linked_lists/sort_list.py` (USES); `tests/test_coverage.py`.

- [ ] **Step 1: Failing test** above `if __name__ == "__main__":`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`: both fail.
- [ ] **Step 3: Move and re-rank.**
  - `git mv` the file into topic 10.
  - Its header becomes `[easy]`, 84 wide.
  - In `_cases`, the big list grows from `range(100_000)` to `range(200_000)`, and its `Aim for:` line says 200,000.
  - Tag it with `count_inversions=recursion.trust,pointers.two_sequences:sort.merge_count`.
  - In `sort_list.py`, USES becomes `["recursion.trust", "pointers.two_sequences", "sort.merge_count", "list.dummy", "list.fast_slow"]`.
- [ ] **Step 4: Registry** (above `    "grid.neighbors": {`):

```python
    "sort.merge_count": {
        "name": "Merge sort, counting while merging",
        "explain": "Split the list in half, sort each half recursively, then merge them with one pointer per half. "
                   "While merging, when the right half's item goes first, it is smaller than every item still "
                   "waiting on the left, so `len(left) - i` pairs can be counted in one step. It's O(n log n).",
    },
```

- [ ] **Step 5: Run** the unit tests (all pass, including Stage 2's `test_topic_10`) and
  `python server.py --check count_inversions sort_list coverage`: two `ok`; `92 techniques, 84 problem(s) not audited yet`.
- [ ] **Step 6: Commit** `Stage 5 audit setup: count_inversions teaches merge sort, from topic 10`.

### Task 2: Topic 26, range queries

- [ ] **Step 1: Failing test:**

```python
    def test_topic_26(self):
        self.assert_audited("26_range_queries")
        self.assert_teaches({"fenwick_prefix": ["fenwick.prefix"], "num_array": ["fenwick.update"],
                             "range_max_updates": ["segtree.basic"], "rank_transform": ["array.rank_compress"]})
        self.assert_uses({"count_smaller": ["fenwick.prefix", "fenwick.update", "array.rank_compress"],
                          "falling_squares": ["segtree.basic", "array.rank_compress"], "reverse_pairs": ["sort.merge_count"],
                          "price_board": ["segtree.basic"], "num_matrix": ["prefix.sums"]})
        for name in ("range_max_updates", "rank_transform"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it: `test_topic_26` fails.
- [ ] **Step 3: Registry:**

```python
    "fenwick.prefix": {
        "name": "Fenwick tree: prefix sums",
        "explain": "A Fenwick tree is a list where `tree[k]` holds the sum of the `k & -k` elements ending at "
                   "position k (counting from 1). To add up the first i elements, take `tree[i]` and strip i's "
                   "lowest set bit, `i -= i & -i`, until i is 0: at most log n steps.",
    },
    "fenwick.update": {
        "name": "Fenwick tree: updates",
        "explain": "To add delta to element k, add it to `tree[k]` and climb to the next block that covers k with "
                   "`k += k & -k`, until k passes n. Together with prefix sums, range sums over changing values "
                   "are O(log n) both ways. To set a value, add the difference from the old one.",
    },
    "segtree.basic": {
        "name": "Segment tree",
        "explain": "A segment tree keeps one value (a max, a sum) for blocks of the array that halve level by level. "
                   "In a list of length 2 · size, the leaves start at size and node i covers nodes 2i and 2i + 1. "
                   "Changing one element fixes the log n nodes above it; a range query combines about 2 log n blocks.",
    },
    "array.rank_compress": {
        "name": "Compressing values to ranks",
        "explain": "When values are huge or spread out but only their order matters, replace each with its rank: "
                   "`rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}`. Then the values can index small "
                   "arrays and trees directly, from 1 up to the number of distinct values.",
    },
```

- [ ] **Step 4: New teachers.** `course/5_advanced_techniques/26_range_queries/range_max_updates.py`:

```python
"""
Range Max With Updates                                                        [easy]

Build a class over a list of numbers:

    MaxArray(nums)
    update(i, val)       set nums[i] = val
    max_range(l, r)      the largest of nums[l..r], both ends included

Example:
    m = MaxArray([2, 7, 1, 8, 3])
    m.max_range(0, 2)   ->  7
    m.update(1, 0)
    m.max_range(0, 2)   ->  2
    m.max_range(1, 4)   ->  8

Aim for:  O(log n) for both. The last test makes 60,000 calls on 50,000 numbers:
          max() over the range is O(n) per call and times out.
Hint:     A segment tree. Put the numbers in the leaves tree[size .. size + n - 1] of a
          list of length 2 * size, and give every node i the max of its children 2i and
          2i + 1. update: set the leaf, then walk up (i //= 2) recomputing each parent.
          max_range: start lo and hi at the two leaves and climb, taking any node that
          sticks out of the range on its side.
"""


class MaxArray:
    def __init__(self, nums: list[int]):
        raise NotImplementedError

    def update(self, i: int, val: int) -> None:
        raise NotImplementedError

    def max_range(self, l: int, r: int) -> int:
        raise NotImplementedError


CLASS = "MaxArray"


def _big():
    import random
    rng = random.Random(2602)
    n = 50_000
    nums = [rng.randint(0, 10**9) for _ in range(n)]
    size = 1
    while size < n:
        size *= 2
    tree = [0] * (2 * size)
    tree[size:size + n] = nums
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[2 * i], tree[2 * i + 1])
    ops, res = [("MaxArray", nums)], [None]
    for _ in range(60_000):
        if rng.random() < 0.5:
            i, v = rng.randrange(n), rng.randint(0, 10**9)
            k = size + i
            tree[k] = v
            k //= 2
            while k:
                tree[k] = max(tree[2 * k], tree[2 * k + 1])
                k //= 2
            ops.append(("update", i, v))
            res.append(None)
        else:
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            lo, hi, best = l + size, r + size + 1, 0
            while lo < hi:
                if lo & 1:
                    best = max(best, tree[lo])
                    lo += 1
                if hi & 1:
                    hi -= 1
                    best = max(best, tree[hi])
                lo //= 2
                hi //= 2
            ops.append(("max_range", l, r))
            res.append(best)
    return ops, res


TEACHES = ["segtree.basic"]
USES = []

TESTS = [
    ([("MaxArray", [2, 7, 1, 8, 3]), ("max_range", 0, 2), ("update", 1, 0), ("max_range", 0, 2), ("max_range", 1, 4)],
     [None, 7, None, 2, 8]),
    ([("MaxArray", [5]), ("max_range", 0, 0), ("update", 0, -3), ("max_range", 0, 0)], [None, 5, None, -3]),
    ([("MaxArray", [-1, -2, -3]), ("max_range", 1, 2), ("update", 2, 9), ("max_range", 0, 1), ("max_range", 0, 2)],
     [None, -2, None, -1, 9]),
    ([("MaxArray", [4, 4, 4, 4, 4, 4]), ("update", 3, 1), ("max_range", 3, 3), ("max_range", 2, 5)],
     [None, None, 1, 4]),
    _big(),
]
```

  `solutions/range_max_updates.py`:

```python
class MaxArray:
    # Iterative segment tree: leaves at size..size+n-1, node i holds the max of nodes 2i and 2i+1.
    def __init__(self, nums: list[int]):
        n, size = len(nums), 1
        while size < n:
            size *= 2
        self.size = size
        self.tree = [float("-inf")] * (2 * size)
        self.tree[size:size + n] = nums
        for i in range(size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i: int, val: int) -> None:
        k = self.size + i
        self.tree[k] = val
        k //= 2
        while k:                                    # every block containing i gets a new max
            self.tree[k] = max(self.tree[2 * k], self.tree[2 * k + 1])
            k //= 2

    def max_range(self, l: int, r: int) -> int:
        lo, hi, best = l + self.size, r + self.size + 1, float("-inf")
        while lo < hi:                              # take the blocks that sit fully inside [l, r]
            if lo & 1:
                best = max(best, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                best = max(best, self.tree[hi])
            lo //= 2
            hi //= 2
        return best
```

  `course/5_advanced_techniques/26_range_queries/rank_transform.py`:

```python
"""
Rank Transform of an Array                                                    [easy]

Replace every number with its rank: 1 for the smallest value, 2 for the next
smallest DIFFERENT value, and so on. Equal numbers get the same rank.

Example:
    rank_transform([40, 10, 20, 30, 10])  ->  [4, 1, 2, 3, 1]

Aim for:  O(n log n). The last test has 100,000 numbers: counting the smaller values
          for every number is O(n²) and times out.
Hint:     Sort the distinct values once: sorted(set(nums)). A dict from each value to its
          position + 1 is the rank table, and every number is then one lookup.
"""


def rank_transform(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(2601)
    nums = [rng.randint(-10**9, 10**9) for _ in range(100_000)]
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    return (nums,), [rank[x] for x in nums]


TEACHES = ["array.rank_compress"]
USES = []

TESTS = [
    (([40, 10, 20, 30, 10],), [4, 1, 2, 3, 1]),
    (([100, 100, 100],), [1, 1, 1]),
    (([],), []),
    (([7],), [1]),
    (([-5, 3, -5, 0],), [1, 3, 1, 2]),
    (([10**9, -10**9],), [2, 1]),
    _big(),
]
```

  `solutions/rank_transform.py`:

```python
def rank_transform(nums: list[int]) -> list[int]:
    # Sort the distinct values once; each value's rank is its position there + 1. O(n log n).
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    return [rank[x] for x in nums]
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/5_advanced_techniques/26_range_queries fenwick_prefix=bits.clear_lowest:fenwick.prefix num_array=fenwick.prefix:fenwick.update range_min_queries= num_matrix=prefix.sums count_smaller=fenwick.prefix,fenwick.update,array.rank_compress falling_squares=segtree.basic,array.rank_compress reverse_pairs=sort.merge_count price_board=segtree.basic
```

- [ ] **Step 6: Run** the unit tests and `--check 26_ coverage`: 10 `ok`; `96 techniques, 76 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 5 audit: topic 26 tagged, with range_max_updates and rank_transform`.

### Task 3: Topic 27, string matching

- [ ] **Step 1: Failing test:**

```python
    def test_topic_27(self):
        self.assert_audited("27_string_matching")
        self.assert_teaches({"prefix_function": ["str.prefix_function"], "find_all": ["str.kmp"]})
        self.assert_uses({"shortest_palindrome": ["str.prefix_function"], "longest_happy_prefix": ["str.prefix_function"],
                          "longest_dup_substring": ["bsearch.first_true", "bsearch.on_answer"], "sum_of_scores": []})
        self.assertEqual(self.problems["longest_happy_prefix"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** it: `test_topic_27` fails.
- [ ] **Step 3: Registry:**

```python
    "str.prefix_function": {
        "name": "The prefix function",
        "explain": "`pi[i]` is the length of the longest proper prefix of `s[:i + 1]` that is also its suffix. Build "
                   "it left to right with k, the current border: while the next character doesn't extend it, fall "
                   "back with `k = pi[k - 1]`. All the fall-backs together are O(n).",
    },
    "str.kmp": {
        "name": "Matching with the prefix function (KMP)",
        "explain": "To find a pattern in a text, build the pattern's prefix function, then walk the text once keeping "
                   "k, how much of the pattern matches right now. On a mismatch, fall back with `k = pi[k - 1]` "
                   "instead of starting over; when k reaches the pattern's length, that's a match. O(text + pattern).",
    },
```

- [ ] **Step 4:** `longest_happy_prefix`'s header becomes `[easy]`, 84 wide.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/5_advanced_techniques/27_string_matching prefix_function=:str.prefix_function find_all=str.prefix_function:str.kmp repeated_substring_pattern=str.prefix_function repeated_dna=hash.seen_set,window.fixed,bits.shift_mask longest_dup_substring=bsearch.first_true,bsearch.on_answer longest_happy_prefix=str.prefix_function shortest_palindrome=str.prefix_function sum_of_scores= shared_phrases=hash.set_lookup,window.fixed
```

- [ ] **Step 6: Run** the unit tests and `--check 27_ coverage`: 9 `ok`; `98 techniques, 67 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 5 audit: topic 27 tagged`.

### Task 4: Topic 28, advanced DP

- [ ] **Step 1: Failing test:**

```python
    def test_topic_28(self):
        self.assert_audited("28_advanced_dynamic_programming")
        self.assert_uses({"ones_and_zeroes": ["dp.knapsack01"], "stock_k_transactions": ["dp.states"],
                          "min_cost_cut_stick": ["dp.interval"], "partition_k_subsets": ["bits.shift_mask", "dp.bitmask"],
                          "stickers_to_spell": ["bfs.shortest", "bfs.implicit", "dp.bitmask"]})
```

- [ ] **Step 2: Run** it: `test_topic_28` fails.
- [ ] **Step 3: Tag.**

```bash
python $TAG course/5_advanced_techniques/28_advanced_dynamic_programming subset_sums=bits.clear_lowest,dp.bitmask shortest_tour=bits.shift_mask,dp.bitmask house_robber_iii=tree.recursion,dp.states ones_and_zeroes=dp.knapsack01 partition_k_subsets=bits.shift_mask,dp.bitmask stock_k_transactions=dp.states min_cost_cut_stick=dp.interval min_palindrome_cuts=dp.prefix,dp.interval stickers_to_spell=bfs.shortest,bfs.implicit,dp.bitmask best_job_schedule=bsearch.first_true,bfs.path,dp.recurrence
```

- [ ] **Step 4: Run** the unit tests and `--check 28_ coverage`: 10 `ok`; `98 techniques, 57 problem(s) not audited yet`.
- [ ] **Step 5: Commit** `Stage 5 audit: topic 28 tagged`.

### Task 5: Topic 29, advanced graphs

- [ ] **Step 1: Failing tests:**

```python
    def test_topic_29(self):
        self.assert_audited("29_advanced_graphs")
        self.assert_teaches({"floyd_step": ["sp.floyd"]})
        self.assert_uses({"city_fewest_reachable": ["sp.floyd"], "has_negative_cycle": ["sp.bellman_ford"],
                          "cracking_safe": ["graph.euler"], "critical_mst_edges": ["uf.find", "uf.union", "graph.mst"],
                          "find_arbitrage": ["bfs.path", "sp.bellman_ford"]})

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
```

- [ ] **Step 2: Run** it: `test_topic_29` fails.
- [ ] **Step 3: Registry:**

```python
    "sp.floyd": {
        "name": "Floyd–Warshall",
        "explain": "For the shortest path between every pair of nodes, allow each node k as a stopover in turn: for "
                   "every pair (i, j), `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. Once every k has "
                   "had its turn, dist holds every shortest distance. It's O(n³).",
    },
```

- [ ] **Step 4: Tag.**

```bash
python $TAG course/5_advanced_techniques/29_advanced_graphs floyd_step=:sp.floyd city_fewest_reachable=sp.floyd is_bipartite=graph.components has_negative_cycle=sp.bellman_ford cracking_safe=graph.euler critical_mst_edges=uf.find,uf.union,graph.mst critical_connections=graph.adjacency min_obstacles=grid.neighbors count_scc=graph.adjacency find_arbitrage=bfs.path,sp.bellman_ford
```

- [ ] **Step 5: Run** the unit tests (all pass) and `--check 29_ coverage`: 10 `ok`; `99 techniques, 47 problem(s) not audited yet`.
- [ ] **Step 6: Commit** `Stage 5 audit: topic 29 tagged`.

### Task 6: README, browser check and full verification

- [ ] **Step 1:** README: `412 coding exercises` becomes `414 coding exercises`.
- [ ] **Step 2:** `tests/browser/stage_5.mjs`, with helpers and opening from `stage_4.mjs`. Checks:
  1. `#/t/26_range_queries`: the list equals `Fenwick tree: prefix sums | Fenwick tree: updates | Segment tree | Compressing values to ranks`.
  2. Solve `fenwick_prefix` and `num_array`.
  3. `#/p/range_max_updates`: `.tech-new h4` is `New technique: Segment tree`.
  4. `#/p/count_smaller`: `.reveal-box` includes `This uses Compressing values to ranks` and `Rank Transform of an Array teaches it`.
  5. `#/p/reverse_pairs`: `.tech-banner` includes `This uses Merge sort, counting while merging` and `Count Inversions`.
  6. No console errors. That is 7 checks.
- [ ] **Step 3:** In `tests/browser/README.md`, add `    bash tests/browser/fresh.sh 8175 stage_5.mjs` after the `stage_4.mjs` line.
- [ ] **Step 4: Run** it: 7 of 7. Then the earlier scenarios (23, 14, 15, 11, 9) and Phase 1 (54).
- [ ] **Step 5:** Unit tests all pass. `python server.py --check`: 414 `ok`, `ok   starting check`, `99 techniques,
  47 problem(s) not audited yet`, `All good.`
- [ ] **Step 6: Commit** `Stage 5 audit: README count and a browser check for topic 26's techniques`.
