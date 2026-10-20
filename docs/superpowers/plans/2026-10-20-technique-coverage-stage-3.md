# Technique coverage, Part 2 Stage 3: audit topics 12–18 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in topics 12–18 lists the techniques it uses. Each of those techniques is
taught by a basic problem that comes earlier, and no Stage 3 problem relies on a later topic.

**Architecture:** Content work only, no server change. 21 techniques join `course/techniques.py`
(67 in all). Every Stage 3 problem file gets `USES` (and `TEACHES` on teachers). Five new easy
teachers and one new hard are added, five problems are re-ranked to easy and one hard becomes a
medium. Two problems move to the topics that teach what they need. A `Stage3Audit` test class pins
all of it.

**Tech Stack:** Python 3.12 stdlib, `unittest`, the existing `--check` self-check, and the Node
headless-Chrome scenarios in `tests/browser/`.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`. The Stage 2 plan,
`docs/superpowers/plans/2026-10-17-technique-coverage-stage-2.md`, is the model for this one; its
Global Constraints all still apply.

## Global Constraints

- No new dependencies. Problem names, topic ids and drill keys never change; files may move between
  topic folders.
- `USES` and `TEACHES` go after the problem's function, class, `PREPARE` and `FINISH`, directly above
  `TESTS =`. `USES` lists techniques in teaching order (enforced by `test_uses_are_in_teaching_order`).
- A teacher is a `snippet`, `guided` or `easy` problem, with exactly one teacher per technique, before
  every user. A technique from a later topic is never allowed.
- Every topic keeps at least two hard problems. Headers are 84 characters wide. Edits keep each
  file's line endings.
- A teacher's big test must time out (2 s per test) for the naive solution a learner without the
  technique would write. **Exceptions in this stage**, because no slower naive solution can be
  measured: `middle_node` and `cycle_start` (fast and slow pointers save space, not time);
  `diameter_of_tree` and `has_path_sum` (the naive versions cost O(n · height), and test trees stay
  under Python's recursion limit); `inorder_traversal` (any correct answer is an in-order walk).
- Tests: `python -m unittest discover -s tests`. Self-check: `python server.py --check <filters>`.
- `TAG` means `C:/Users/sam/AppData/Local/Temp/claude/C--Users-sam-Desktop-dsa/37698c59-d18f-494f-9d0b-cad64d5356c4/scratchpad/s2/tag.py`
  (created in Stage 2; its code is in the Stage 1 plan, Task 1 Step 6, if it is gone).
- End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Audit results

Read for every Stage 3 problem: statement, hint and reference solution.

**New techniques (21), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `stack.lifo` | Stack: last in, first out | `bracket_step` (snippet, 12) | reuse |
| `stack.monotonic` | Monotonic stack | `daily_temperatures` | **re-rank** medium → easy; `largest_rectangle` and `maximal_rectangle` rely on it |
| `deque.monotonic` | Monotonic deque | `sliding_window_max` | **re-rank** hard → easy: the spec's gap 3, it came after the two hards that rely on it |
| `list.reverse` | Reversing links | `reverse_between` (guided, 14) | reuse |
| `list.dummy` | Dummy head node | `reverse_between` (guided, 14) | reuse |
| `list.fast_slow` | Fast and slow pointers | `middle_node` (easy, 14) | reuse |
| `list.recency` | Recency order: dict plus linked list | `recently_used` | **new** easy in 14: `lfu_cache` and `lru_cache` rely on it |
| `list.cycle_start` | Finding where a cycle starts | `cycle_start` | **new** easy in 14: the spec's gap for `find_duplicate` |
| `tree.recursion` | Tree recursion | `count_nodes` (snippet, 15) | reuse |
| `tree.bfs_levels` | Level-by-level BFS | `right_side_view` (guided, 15) | reuse |
| `tree.return_and_record` | Return one thing, record another | `diameter_of_tree` | **re-rank** medium → easy; `min_cameras`, `max_path_sum` and `max_sum_bst` rely on it |
| `tree.carry_down` | Passing values down a path | `has_path_sum` (easy, 15) | reuse |
| `bst.walk_down` | Walking down a BST | `bst_insert` (snippet, 16) | reuse |
| `tree.inorder` | In-order traversal | `inorder_traversal` | **new** easy in 16, which had none: four problems rely on in-order order |
| `heap.top_k` | Keeping the k largest | `push_keep_k` (snippet, 17) | reuse |
| `heap.max_negate` | Max-heap by negating | `last_stone` (guided, 17) | reuse |
| `heap.two_heaps` | Two heaps for the median | `median_finder` | **re-rank** hard → easy: the spec's gap; `sliding_window_median` relies on it |
| `heap.lazy_delete` | Lazy deletion | `max_bag` | **new** easy in 17: the spec's gap; `skyline`, `sliding_window_median`, `min_interval_query` and `task_scheduler` rely on it |
| `heap.k_way_merge` | Merging sorted lists with a heap | `k_smallest_sums` | **new** easy in 17: `twitter` and `merge_k_sorted` rely on it, and `sorted()` can't pass this one |
| `trie.walk` | Walking a trie | `trie_insert` (snippet, 18) | reuse |
| `trie.counts` | Counting words through a trie node | `count_prefixes` | **re-rank** medium → easy; `word_dictionary` relies on it |

**Other rank changes.** `merge_k_sorted` becomes a medium: with `k_smallest_sums` teaching the
merge, it has no insight of its own left for a hard.

**Moved to the topic of their last prerequisite** (Stage 4 tags them there):

| Problem | From | To | Needs |
|---|---|---|---|
| `word_search_ii` | 18 | `22_backtracking` | grid DFS with mark and unmark (19, 22) |
| `concatenated_words` | 18 | `23_dynamic_programming_1d` | a word-break DP |

Topic 18 then has one hard left, so **one new hard** joins it: `stream_matches` (Stream of
Characters), which uses only a trie of the reversed words.

**Judgment call for the reviewer.** `maximal_rectangle`'s hint hands off to "Largest Rectangle in
Histogram", the hard just before it. It is tagged with `stack.monotonic` and keeps "each row is a
histogram's floor" as its own insight. The histogram step is `largest_rectangle`'s own insight and
isn't a technique, because a hard can't teach. The ladder puts `largest_rectangle` first.

**Tags for every problem.** USES is written in teaching order.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 12 | `bracket_step` (snippet) | `stack.lifo` | | |
| 12 | `simplify_path` (guided), `valid_parentheses`, `eval_rpn`, `text_editor` (build) | | `stack.lifo` | |
| 12 | `daily_temperatures` (now easy) | `stack.monotonic` | `stack.lifo` | |
| 12 | `car_fleet` | | `scan.best_so_far` | own: sort by position, compare arrival times |
| 12 | `min_stack` | | `stack.lifo` | own: store the minimum with each item |
| 12 | `largest_rectangle` (hard) | | `stack.monotonic` | own: a popped bar's width runs to the new top |
| 12 | `longest_valid_parentheses` (hard) | | `stack.lifo` | own: an index sentinel at the bottom |
| 12 | `maximal_rectangle` (hard) | | `stack.monotonic` | see the judgment call |
| 13 | `expire_old` (snippet) | | `window.variable` | |
| 13 | `moving_average` (guided) | | `window.fixed` | |
| 13 | `first_unique_char` | | | `Counter` |
| 13 | `sliding_window_max` (now easy) | `deque.monotonic` | `window.fixed`, `stack.monotonic` | |
| 13 | `max_value_of_equation` (hard) | | `pairs.split_by_index`, `window.variable`, `deque.monotonic` | |
| 13 | `shortest_subarray_at_least_k` (hard) | | `prefix.sums`, `deque.monotonic` | own: pop the front once it's good enough |
| 13 | `ticket_queue` (build) | | `hash.set_lookup` | |
| 14 | `insert_after` (snippet) | | | |
| 14 | `reverse_between` (guided) | `list.reverse`, `list.dummy` | | |
| 14 | `merge_two_lists` | | `pointers.two_sequences`, `list.dummy` | |
| 14 | `middle_node` | `list.fast_slow` | | |
| 14 | `recently_used` (new) | `list.recency` | | |
| 14 | `reverse_list` | | `list.reverse` | |
| 14 | `has_cycle` | | `list.fast_slow` | own: the fast pointer laps the slow one |
| 14 | `cycle_start` (new) | `list.cycle_start` | `list.fast_slow` | |
| 14 | `add_two_numbers` | | `math.carry`, `list.dummy` | |
| 14 | `copy_random_list` | | | own: a dict from each old node to its copy |
| 14 | `find_duplicate` | | `list.fast_slow`, `list.cycle_start` | own: read each value as a next pointer |
| 14 | `remove_nth_from_end` | | `list.dummy` | own: keep a gap of n nodes |
| 14 | `reorder_list` | | `pointers.two_sequences`, `list.reverse`, `list.fast_slow` | |
| 14 | `lfu_cache` (hard), `lru_cache` (build) | | `list.recency` | `lfu_cache` own: one recency list per count, and the minimum count |
| 14 | `reverse_k_group` (hard) | | `list.reverse`, `list.dummy` | own: reconnect each group |
| 14 | `sort_list` (hard) | | `recursion.trust`, `pointers.two_sequences`, `list.dummy`, `list.fast_slow` | own: merge sort |
| 15 | `count_nodes` (snippet) | `tree.recursion` | `recursion.trust` | |
| 15 | `right_side_view` (guided) | `tree.bfs_levels` | | |
| 15 | `invert_tree`, `max_depth`, `same_tree` | | `tree.recursion` | |
| 15 | `is_balanced` | | `tree.recursion` | own: −1 means "unbalanced below" |
| 15 | `is_subtree` | | `tree.recursion` | own: check "same tree" at every node |
| 15 | `diameter_of_tree` (now easy) | `tree.return_and_record` | `tree.recursion` | |
| 15 | `has_path_sum` | `tree.carry_down` | `tree.recursion` | |
| 15 | `level_order` | | `tree.bfs_levels` | |
| 15 | `build_tree_pre_in` | | `tree.recursion` | own: the root splits the inorder list |
| 15 | `good_nodes` | | `tree.carry_down` | |
| 15 | `min_cameras`, `max_path_sum` (hard) | | `tree.return_and_record` | own: three states; gain versus bend |
| 15 | `serialize_tree` (hard) | | `recursion.parse`, `tree.recursion` | own: preorder with empty markers |
| 15 | `vertical_traversal` (hard) | | `tree.carry_down` | own: sort (col, row, value) and group |
| 15 | `org_chart` (build) | | `hash.group_key`, `tree.recursion` | |
| 16 | `bst_insert` (snippet) | `bst.walk_down` | | |
| 16 | `bst_range_sum` (guided), `lowest_common_ancestor` | | `bst.walk_down` | own: skip whole subtrees; where p and q split |
| 16 | `inorder_traversal` (new) | `tree.inorder` | `tree.recursion` | |
| 16 | `kth_smallest_bst`, `recover_bst` (hard) | | `tree.inorder` | `recover_bst` own: find the drops |
| 16 | `is_valid_bst` | | `tree.carry_down` | own: a range each node must fit |
| 16 | `closest_k_values` (hard) | | `window.fixed`, `tree.inorder` | own: stop once a value isn't closer |
| 16 | `max_sum_bst` (hard) | | `tree.return_and_record` | own: return (is BST, min, max, sum) |
| 16 | `tree_set` (build) | | `bst.walk_down`, `tree.inorder` | |
| 17 | `push_keep_k` (snippet) | `heap.top_k` | | |
| 17 | `last_stone` (guided) | `heap.max_negate` | | |
| 17 | `median_finder` (now easy) | `heap.two_heaps` | `heap.max_negate` | |
| 17 | `kth_largest_stream`, `kth_largest` | | `heap.top_k` | |
| 17 | `max_bag` (new) | `heap.lazy_delete` | `heap.max_negate` | |
| 17 | `k_smallest_sums` (new) | `heap.k_way_merge` | | |
| 17 | `twitter` | | `heap.max_negate`, `heap.k_way_merge` | |
| 17 | `k_closest` | | `heap.top_k`, `heap.max_negate` | |
| 17 | `merge_k_sorted` (now medium) | | `heap.k_way_merge` | |
| 17 | `min_meeting_rooms` | | `intervals.sort_by_start` | own: a min-heap of end times |
| 17 | `least_interval` | | | own: the frame the most frequent task sets |
| 17 | `min_interval_query` (hard) | | `intervals.sort_by_start`, `heap.lazy_delete` | own: answer the queries in sorted order |
| 17 | `sliding_window_median` (hard) | | `window.fixed`, `heap.max_negate`, `heap.two_heaps`, `heap.lazy_delete` | own: count the valid items per heap |
| 17 | `skyline` (hard), `task_scheduler` (build) | | `heap.max_negate`, `heap.lazy_delete` | `skyline` own: sweep the x values where something changes |
| 18 | `trie_insert` (snippet) | `trie.walk` | | |
| 18 | `autocomplete` (guided) | | `bsearch.first_true` | own: sorted words with a prefix sit together |
| 18 | `count_prefixes` (now easy) | `trie.counts` | `trie.walk` | |
| 18 | `implement_trie` | | `trie.walk` | |
| 18 | `replace_words` | | `trie.walk` | own: stop at the first word end |
| 18 | `palindrome_pairs` (hard) | | `hash.complement` | own: split each word at every cut |
| 18 | `stream_matches` (new hard) | | `trie.walk` | own: reverse the words, walk back from the newest letter |
| 18 | `word_dictionary` (build) | | `recursion.trust`, `trie.walk`, `trie.counts` | own: branch on "." |

**Known limit.** `count_prefixes` can be passed by counting every prefix of every word in a
`Counter`, a hashing method from topic 04. Its big test rejects scanning every word for every
prefix.

## Review Focus

1. **Moved problems keep their history.** `word_search_ii` and `concatenated_words` keep progress
   and study-plan entries. Owners: `test_problems_moved_to_the_topic_of_their_last_prerequisite` and
   `test_every_plan_item_exists`.
2. **The lock walks the teachers in order.** On `sliding_window_median`, the lock names "Find Median
   from Data Stream" first, then "Max With Removals" once that is solved. Owners:
   `test_uses_are_in_teaching_order`, and the Task 9 browser check.
3. **A teacher can't be passed without its technique**, apart from the listed exceptions. Owner: the
   Task 8 test `test_teacher_big_tests_reject_the_naive_solution`. Every naive version was timed at
   over 2 s while this plan was written: list `remove` (`recently_used`), `max()` over a list and a
   sorted list (`max_bag`), the k × k sums, scanning every word and checking every length
   (`stream_matches`), O(n²) scans (`daily_temperatures`, `count_prefixes`), and `insort`
   (`median_finder`, 4.8 s on its existing 150,000-call test).
4. **Re-ranking and moving keep two hards in every Stage 3 topic.** Owner: the Task 8 test
   `test_every_stage_3_topic_keeps_two_hard_problems`.
5. **Class and linked-list teachers behave like the rest.** `recently_used` and `max_bag` use the
   `CLASS` op format, and `cycle_start` uses `PREPARE`/`FINISH`. Owner: `--check` in Tasks 4 and 7.

---

### Task 1: The moves and the test class

**Files:** `tests/test_coverage.py` (new `Stage3Audit`); move `course/3_data_structures/18_tries/word_search_ii.py`
→ `course/4_advanced/22_backtracking/`, and `concatenated_words.py` → `course/4_advanced/23_dynamic_programming_1d/`;
`docs/superpowers/specs/2026-10-16-technique-coverage-design.md`.

**Interfaces:** Produces `Stage3Audit(AuditBase)` and `STAGE_3`. Tasks 2–8 add methods to it.

- [ ] **Step 1: Write the failing test.** Above `if __name__ == "__main__":` in `tests/test_coverage.py`:

```python
STAGE_3 = ("12_stacks", "13_queues_and_deques", "14_linked_lists", "15_trees", "16_binary_search_trees",
           "17_heaps", "18_tries")


class Stage3Audit(AuditBase):
    """Part 2, Stage 3: topics 12-18 fully audited (docs/superpowers/plans/2026-10-20-technique-coverage-stage-3.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        for name, topic_id in (("word_search_ii", "22_backtracking"), ("concatenated_words", "23_dynamic_programming_1d")):
            self.assertEqual(self.problems[name]["topic_id"], topic_id, name)
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected: the move
  test fails with `'18_tries' != '22_backtracking'`.
- [ ] **Step 3: Move** both files with `git mv`. Check that nothing else names them by topic:
  `grep -rn "word_search_ii\|concatenated_words" web course/*/*/lesson.py` should print nothing.
- [ ] **Step 4: Update the spec.**
  - The table row for "finding where a cycle starts": add ` (fixed: the new \`cycle_start\` teaches it)` to its last cell.
  - The row for "two heaps for the median": add ` (fixed: \`median_finder\`, now easy, teaches it)`.
  - The row for "lazy deletion": add ` (fixed: the new \`max_bag\` teaches it)`.
  - The rows for `word_search_ii` (18) and `concatenated_words` (18): add ` (fixed: moved there)` to the last cell.
  - The paragraph that starts `**3. Basic versions sorted after their users.**`: append
    ` Fixed in Stage 3: \`sliding_window_max\` is now the easy problem that teaches the monotonic deque.`
  - Under "What a teaching problem looks like", after the bullet about its hint and reference
    solution, add: `- Its big test times out for the naive solution a learner without the technique would write. The exceptions are techniques that save only space, or whose naive version is slow only on inputs too deep to test; each stage plan lists them.`
- [ ] **Step 5: Run** `python -m unittest discover -s tests`. Expected: all pass. Then
  `python server.py --check word_search_ii concatenated_words coverage`. Expected: two `ok` lines
  under topics 22 and 23; `46 techniques, 248 problem(s) not audited yet`; `All good.`
- [ ] **Step 6: Commit** `git add tests/test_coverage.py course docs/superpowers/specs/2026-10-16-technique-coverage-design.md`,
  message `Stage 3 audit setup: word_search_ii and concatenated_words moved to the topics they need`.

### Task 2: Topic 12, stacks

**Files:** `course/techniques.py` (2 entries); `12_stacks/daily_temperatures.py` (re-rank, big test); every
problem file in `12_stacks/` (tags); `tests/test_coverage.py`.

- [ ] **Step 1: Failing test** in `Stage3Audit`:

```python
    def test_topic_12(self):
        self.assert_audited("12_stacks")
        self.assert_teaches({"bracket_step": ["stack.lifo"], "daily_temperatures": ["stack.monotonic"]})
        self.assert_uses({"car_fleet": ["scan.best_so_far"], "largest_rectangle": ["stack.monotonic"],
                          "maximal_rectangle": ["stack.monotonic"], "text_editor": ["stack.lifo"]})
        self.assertEqual(self.problems["daily_temperatures"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected: `test_topic_12` fails.
- [ ] **Step 3: Registry** — insert above `    "grid.neighbors": {`:

```python
    "stack.lifo": {
        "name": "Stack: last in, first out",
        "explain": "A Python list is a stack: `append` puts an item on top and `pop` takes the top off, both O(1). "
                   "Use one whenever the most recent unfinished thing must be dealt with first: the last opened "
                   "bracket, the folder you just went into, the last edit to undo.",
    },
    "stack.monotonic": {
        "name": "Monotonic stack",
        "explain": "Keep a stack of indexes whose values only go down. When a new value is bigger than the top, "
                   "pop until it isn't: each popped index has just found its next bigger value, the new one. Every "
                   "index is pushed and popped once, so the scan is O(n). Flip the comparison for the next smaller.",
    },
```

- [ ] **Step 4: Re-rank `daily_temperatures`.** Header becomes `Daily Temperatures` padded to 84 with
  `[easy]` (it was 85 wide, with `[medium] · stack`). Replace `Aim for:  O(n) time` with
  `Aim for:  O(n) time. The last test has 100,000 falling temperatures: looking ahead from every` and
  `          day is O(n²) and times out.`. Add the last test `((list(range(100_000, 0, -1)),), [0] * 100_000),`.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/3_data_structures/12_stacks bracket_step=:stack.lifo simplify_path=stack.lifo valid_parentheses=stack.lifo daily_temperatures=stack.lifo:stack.monotonic car_fleet=scan.best_so_far eval_rpn=stack.lifo min_stack=stack.lifo largest_rectangle=stack.monotonic longest_valid_parentheses=stack.lifo maximal_rectangle=stack.monotonic text_editor=stack.lifo
```

  Expected: 11 `tagged` lines.
- [ ] **Step 6: Run** the unit tests (all pass) and `python server.py --check 12_ coverage`. Expected:
  11 `ok`; `48 techniques, 237 problem(s) not audited yet`; `All good.`
- [ ] **Step 7: Commit** `Stage 3 audit: topic 12 tagged` / `daily_temperatures is now easy and teaches the monotonic stack.`

### Task 3: Topic 13, queues and deques

**Files:** `course/techniques.py` (1 entry); `13_queues_and_deques/sliding_window_max.py` (re-rank); every problem file (tags).

- [ ] **Step 1: Failing test:**

```python
    def test_topic_13(self):
        self.assert_audited("13_queues_and_deques")
        self.assert_teaches({"sliding_window_max": ["deque.monotonic"]})
        self.assert_uses({"max_value_of_equation": ["pairs.split_by_index", "window.variable", "deque.monotonic"],
                          "shortest_subarray_at_least_k": ["prefix.sums", "deque.monotonic"],
                          "expire_old": ["window.variable"], "ticket_queue": ["hash.set_lookup"]})
        self.assertEqual(self.problems["sliding_window_max"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** it. Expected: `test_topic_13` fails.
- [ ] **Step 3: Registry:**

```python
    "deque.monotonic": {
        "name": "Monotonic deque",
        "explain": "For the maximum of a sliding window, keep a deque of indexes whose values go down from front to "
                   "back. Before adding a new index, pop smaller values off the back: they can never be the max "
                   "again. Pop the front once it slides out of the window. The front is always the window's max.",
    },
```

- [ ] **Step 4: Re-rank `sliding_window_max`:** `[hard]` becomes `[easy]` (same width). Its big test already rejects O(n·k).
- [ ] **Step 5: Tag.**

```bash
python $TAG course/3_data_structures/13_queues_and_deques expire_old=window.variable moving_average=window.fixed first_unique_char= sliding_window_max=window.fixed,stack.monotonic:deque.monotonic max_value_of_equation=pairs.split_by_index,window.variable,deque.monotonic shortest_subarray_at_least_k=prefix.sums,deque.monotonic ticket_queue=hash.set_lookup
```

- [ ] **Step 6: Run** the unit tests and `--check 13_ coverage`. Expected: 7 `ok`; `49 techniques, 230 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 3 audit: topic 13 tagged` / `sliding_window_max is now the easy problem that teaches the monotonic deque, before the two hards that rely on it.`

### Task 4: Topic 14, linked lists

**Files:** `course/techniques.py` (5 entries); create `14_linked_lists/cycle_start.py`, `recently_used.py` and their
solutions; every other problem file (tags).

- [ ] **Step 1: Failing test:**

```python
    def test_topic_14(self):
        self.assert_audited("14_linked_lists")
        self.assert_teaches({"reverse_between": ["list.reverse", "list.dummy"], "middle_node": ["list.fast_slow"],
                             "recently_used": ["list.recency"], "cycle_start": ["list.cycle_start"]})
        self.assert_uses({"find_duplicate": ["list.fast_slow", "list.cycle_start"], "lfu_cache": ["list.recency"],
                          "merge_two_lists": ["pointers.two_sequences", "list.dummy"],
                          "sort_list": ["recursion.trust", "pointers.two_sequences", "list.dummy", "list.fast_slow"]})
        for name in ("recently_used", "cycle_start"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it. Expected: `test_topic_14` fails.
- [ ] **Step 3: Registry:**

```python
    "list.reverse": {
        "name": "Reversing links",
        "explain": "Walk the list with `prev`, `curr` and `nxt`: save `nxt = curr.next`, point `curr.next` back at "
                   "`prev`, then step both forward. When curr falls off the end, prev is the new head. Save the next "
                   "node before you overwrite the link, or the rest of the list is lost.",
    },
    "list.dummy": {
        "name": "Dummy head node",
        "explain": "Put a throwaway node in front of the head: `dummy = ListNode(0, head)`. Now every real node, the "
                   "first one included, has a node before it, so inserting or removing at the head needs no special "
                   "case. Return `dummy.next` at the end.",
    },
    "list.fast_slow": {
        "name": "Fast and slow pointers",
        "explain": "Move `slow` one node and `fast` two nodes per step. When fast reaches the end, slow is in the "
                   "middle. If the list loops, fast laps slow and they land on the same node. One pass, O(1) extra "
                   "space.",
    },
    "list.recency": {
        "name": "Recency order: dict plus linked list",
        "explain": "To keep keys ordered by when they were last used, pair a dict with a doubly linked list: the dict "
                   "finds a key's node in O(1), and the list moves it to the newest end or drops the oldest in O(1). "
                   "`collections.OrderedDict` is exactly this: `move_to_end(key)` and `popitem(last=False)`.",
    },
    "list.cycle_start": {
        "name": "Finding where a cycle starts",
        "explain": "Once fast and slow have met inside the loop, put one pointer back at the head and move both one "
                   "step at a time. They meet exactly where the loop begins: the head is as far from the loop's "
                   "start as the meeting point is, going round.",
    },
```

- [ ] **Step 4: New teachers.** `course/3_data_structures/14_linked_lists/cycle_start.py`:

```python
"""
Where the Cycle Starts                                                        [easy]

The linked list may loop back on itself. Return the node where the loop
begins (the first node you would reach twice), or None if there's no loop.

Each test is (values, pos): the tail points back to the node at index pos,
or nowhere if pos is -1. Values are all different, and the test reads the
value of the node you return.

Example:
    3 -> 2 -> 0 -> -4
         ^__________|       cycle_start(head)  ->  the node holding 2

Aim for:  O(n) time, O(1) space. A set of visited nodes works, but uses O(n) space.
Hint:     First move fast and slow pointers until they meet, as in "Linked List
          Cycle". Then put one pointer back at the head and move both one step
          at a time: they meet exactly where the loop begins.
"""
from helpers import ListNode, build_list


def cycle_start(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, pos):
    return (build_list(values, cycle_to=pos),)


def FINISH(node):
    return None if node is None else node.val


TEACHES = ["list.cycle_start"]
USES = ["list.fast_slow"]

TESTS = [
    (([3, 2, 0, -4], 1), 2),
    (([1, 2], 0), 1),
    (([1], 0), 1),
    (([1], -1), None),
    (([], -1), None),
    (([1, 2, 3, 4, 5], -1), None),
    ((list(range(10)), 7), 7),
    ((list(range(10_000)), 3_000), 3_000),
]
```

  `solutions/cycle_start.py`:

```python
def cycle_start(head):
    # Phase 1: fast and slow meet inside the loop. Phase 2: from the head and from the
    # meeting point, both one step at a time, they meet where the loop begins. O(n), O(1).
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```

  `course/3_data_structures/14_linked_lists/recently_used.py`:

```python
"""
Recently Used Order                                                           [easy]

Keep keys in the order they were last used:

    use(key)        mark key as the most recently used (adding it if it's new)
    oldest()        the least recently used key, or None if there are none
    drop_oldest()   remove the least recently used key and return it (None if empty)

Example:
    r = RecentlyUsed()
    r.use("a"); r.use("b"); r.use("a")
    r.oldest()        ->  "b"       "a" was used again after "b"
    r.drop_oldest()   ->  "b"
    r.oldest()        ->  "a"

Aim for:  O(1) for every call. The last test makes 200,000 calls: keeping the keys
          in a list and calling list.remove on every use is O(n) and times out.
Hint:     A dict finds a key's place in O(1), and a doubly linked list moves it to
          the end in O(1). collections.OrderedDict is both at once: move_to_end(key)
          on a use, next(iter(d)) for the oldest, popitem(last=False) to drop it.
"""


class RecentlyUsed:
    def __init__(self):
        raise NotImplementedError

    def use(self, key: str) -> None:
        raise NotImplementedError

    def oldest(self) -> str | None:
        raise NotImplementedError

    def drop_oldest(self) -> str | None:
        raise NotImplementedError


CLASS = "RecentlyUsed"


def _big():
    import random
    from collections import OrderedDict
    rng = random.Random(1403)
    d, ops, res = OrderedDict(), [("RecentlyUsed",)], [None]
    for _ in range(200_000):
        r = rng.random()
        if r < 0.8:
            key = f"k{rng.randrange(60_000)}"
            d[key] = None
            d.move_to_end(key)
            ops.append(("use", key))
            res.append(None)
        elif r < 0.9:
            ops.append(("oldest",))
            res.append(next(iter(d)) if d else None)
        else:
            ops.append(("drop_oldest",))
            res.append(d.popitem(last=False)[0] if d else None)
    return ops, res


TEACHES = ["list.recency"]
USES = []

TESTS = [
    ([("RecentlyUsed",), ("use", "a"), ("use", "b"), ("use", "a"), ("oldest",), ("drop_oldest",), ("oldest",)],
     [None, None, None, None, "b", "b", "a"]),
    ([("RecentlyUsed",), ("oldest",), ("drop_oldest",)], [None, None, None]),
    ([("RecentlyUsed",), ("use", "x"), ("drop_oldest",), ("oldest",), ("use", "x"), ("use", "y"), ("use", "z"),
      ("use", "y"), ("drop_oldest",), ("drop_oldest",), ("oldest",)],
     [None, None, "x", None, None, None, None, None, "x", "z", "y"]),
    _big(),
]
```

  `solutions/recently_used.py`:

```python
from collections import OrderedDict


class RecentlyUsed:
    # An OrderedDict is a dict plus a doubly linked list: O(1) lookup, O(1) move to the end.
    def __init__(self):
        self.order = OrderedDict()          # least recently used first

    def use(self, key: str) -> None:
        self.order[key] = None
        self.order.move_to_end(key)

    def oldest(self) -> str | None:
        return next(iter(self.order), None)

    def drop_oldest(self) -> str | None:
        return self.order.popitem(last=False)[0] if self.order else None
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/3_data_structures/14_linked_lists insert_after= reverse_between=:list.reverse,list.dummy has_cycle=list.fast_slow merge_two_lists=pointers.two_sequences,list.dummy middle_node=:list.fast_slow reverse_list=list.reverse add_two_numbers=math.carry,list.dummy copy_random_list= find_duplicate=list.fast_slow,list.cycle_start remove_nth_from_end=list.dummy reorder_list=pointers.two_sequences,list.reverse,list.fast_slow lfu_cache=list.recency reverse_k_group=list.reverse,list.dummy sort_list=recursion.trust,pointers.two_sequences,list.dummy,list.fast_slow lru_cache=list.recency
```

  Expected: 15 `tagged` lines.
- [ ] **Step 6: Run** the unit tests and `--check 14_ coverage`. Expected: 17 `ok`; `54 techniques, 215 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 3 audit: topic 14 tagged, with cycle_start and recently_used` /
  `Finding where a cycle starts and keeping recency order get basic problems before find_duplicate, lfu_cache and lru_cache rely on them.`

### Task 5: Topic 15, trees

**Files:** `course/techniques.py` (4 entries); `15_trees/diameter_of_tree.py` (re-rank); every problem file (tags).

- [ ] **Step 1: Failing test:**

```python
    def test_topic_15(self):
        self.assert_audited("15_trees")
        self.assert_teaches({"count_nodes": ["tree.recursion"], "right_side_view": ["tree.bfs_levels"],
                             "diameter_of_tree": ["tree.return_and_record"], "has_path_sum": ["tree.carry_down"]})
        self.assert_uses({"max_path_sum": ["tree.return_and_record"], "min_cameras": ["tree.return_and_record"],
                          "good_nodes": ["tree.carry_down"], "serialize_tree": ["recursion.parse", "tree.recursion"],
                          "level_order": ["tree.bfs_levels"]})
        self.assertEqual(self.problems["diameter_of_tree"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** it. Expected: `test_topic_15` fails.
- [ ] **Step 3: Registry:**

```python
    "tree.recursion": {
        "name": "Tree recursion",
        "explain": "Answer for an empty tree (None) directly. For a real node, call the function on `node.left` and "
                   "`node.right`, trust both answers, and combine them with the node's own value: "
                   "`1 + count(node.left) + count(node.right)`. Most tree problems are this template.",
    },
    "tree.bfs_levels": {
        "name": "Level-by-level BFS",
        "explain": "Put the root in a deque. At the start of each round, `len(queue)` is the number of nodes on the "
                   "current level: pop exactly that many, handle them, and push their children. Each round is one "
                   "level, top to bottom.",
    },
    "tree.return_and_record": {
        "name": "Return one thing, record another",
        "explain": "Sometimes the parent needs one value (a height) but the answer is another (the longest path "
                   "through some node). Have the helper return what the parent needs and update a `best` variable "
                   "on the side, with `nonlocal`. One walk does both.",
    },
    "tree.carry_down": {
        "name": "Passing values down a path",
        "explain": "When a node's answer depends on what's above it (the sum so far, the biggest value above it, the "
                   "range it must fit in), pass that as an extra argument on the way down: "
                   "`walk(child, total + node.val)`. Each node then knows its whole path in O(1).",
    },
```

- [ ] **Step 4: Re-rank `diameter_of_tree`:** `[medium]` becomes `  [easy]` (stays 84 wide).
- [ ] **Step 5: Tag.**

```bash
python $TAG course/3_data_structures/15_trees count_nodes=recursion.trust:tree.recursion right_side_view=:tree.bfs_levels is_balanced=tree.recursion invert_tree=tree.recursion max_depth=tree.recursion has_path_sum=tree.recursion:tree.carry_down same_tree=tree.recursion is_subtree=tree.recursion level_order=tree.bfs_levels build_tree_pre_in=tree.recursion good_nodes=tree.carry_down diameter_of_tree=tree.recursion:tree.return_and_record min_cameras=tree.return_and_record max_path_sum=tree.return_and_record serialize_tree=recursion.parse,tree.recursion vertical_traversal=tree.carry_down org_chart=hash.group_key,tree.recursion
```

  Expected: 17 `tagged` lines.
- [ ] **Step 6: Run** the unit tests and `--check 15_ coverage`. Expected: 17 `ok`; `58 techniques, 198 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 3 audit: topic 15 tagged` / `diameter_of_tree is now easy and teaches returning one value while recording another.`

### Task 6: Topic 16, binary search trees

**Files:** `course/techniques.py` (2 entries); create `16_binary_search_trees/inorder_traversal.py` and its solution;
every other problem file (tags).

- [ ] **Step 1: Failing test:**

```python
    def test_topic_16(self):
        self.assert_audited("16_binary_search_trees")
        self.assert_teaches({"bst_insert": ["bst.walk_down"], "inorder_traversal": ["tree.inorder"]})
        self.assert_uses({"kth_smallest_bst": ["tree.inorder"], "closest_k_values": ["window.fixed", "tree.inorder"],
                          "max_sum_bst": ["tree.return_and_record"], "is_valid_bst": ["tree.carry_down"],
                          "tree_set": ["bst.walk_down", "tree.inorder"]})
        self.assertEqual(self.problems["inorder_traversal"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** it. Expected: `test_topic_16` fails.
- [ ] **Step 3: Registry:**

```python
    "bst.walk_down": {
        "name": "Walking down a BST",
        "explain": "In a binary search tree everything smaller sits to the left and everything bigger to the right. "
                   "So searching, inserting and many queries walk one path from the root: left if the target is "
                   "smaller, right if bigger. That's O(height), and whole subtrees get skipped.",
    },
    "tree.inorder": {
        "name": "In-order traversal",
        "explain": "Visit the left subtree, then the node, then the right subtree. On a binary search tree that gives "
                   "the values in increasing order. With your own stack: go left as far as you can, pushing nodes; "
                   "pop one, visit it, then do the same from its right child. You can stop early.",
    },
```

- [ ] **Step 4: New teacher.** `course/3_data_structures/16_binary_search_trees/inorder_traversal.py`:

```python
"""
Inorder Traversal                                                             [easy]

Return the values of a binary tree in in-order: everything in the left
subtree, then the node itself, then everything in the right subtree.

Example:
        1
         \\
          2         ->  [1, 3, 2]
         /
        3

Trees are in level order with None for missing children (see helpers).

Aim for:  O(n). Write it recursively first, then with your own stack.
Hint:     Recursively: inorder(left) + [node.val] + inorder(right). With a stack:
          go left as far as you can, pushing each node; pop one, record it, then
          do the same from its right child.
"""
from helpers import TreeNode, build_tree


def inorder_traversal(root: TreeNode | None) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


TEACHES = ["tree.inorder"]
USES = ["tree.recursion"]

TESTS = [
    (([1, None, 2, 3],), [1, 3, 2]),
    (([],), []),
    (([1],), [1]),
    (([1, 2, 3, 4, 5, None, 6],), [4, 2, 5, 1, 3, 6]),
    (([5, 3, 8, 1, 4, 7, 9],), [1, 3, 4, 5, 7, 8, 9]),
    (([2, 9, 4, None, 7, 1],), [9, 7, 2, 1, 4]),
]
```

  `solutions/inorder_traversal.py`:

```python
def inorder_traversal(root) -> list[int]:
    # Go left as far as possible, then visit, then turn right. On a BST this is sorted order. O(n).
    out, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/3_data_structures/16_binary_search_trees bst_insert=:bst.walk_down bst_range_sum=bst.walk_down kth_smallest_bst=tree.inorder lowest_common_ancestor=bst.walk_down is_valid_bst=tree.carry_down closest_k_values=window.fixed,tree.inorder max_sum_bst=tree.return_and_record recover_bst=tree.inorder tree_set=bst.walk_down,tree.inorder
```

- [ ] **Step 6: Run** the unit tests and `--check 16_ coverage`. Expected: 10 `ok`; `60 techniques, 189 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 3 audit: topic 16 tagged, with inorder_traversal` / `In-order traversal gets a basic problem before four BST problems rely on it.`

### Task 7: Topic 17, heaps

**Files:** `course/techniques.py` (5 entries); create `17_heaps/max_bag.py`, `k_smallest_sums.py` and their solutions;
`median_finder.py` (re-rank to easy, header to 84), `merge_k_sorted.py` (hard → medium); every problem file (tags).

- [ ] **Step 1: Failing tests:**

```python
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
```

- [ ] **Step 2: Run** it. Expected: `test_topic_17` fails.
- [ ] **Step 3: Registry:**

```python
    "heap.top_k": {
        "name": "Keeping the k largest",
        "explain": "To track the k largest values, keep a MIN-heap of at most k of them: push each new value, and pop "
                   "when the heap grows past k. The smallest of the k largest, the kth largest, sits on top at "
                   "`heap[0]`. O(log k) per value.",
    },
    "heap.max_negate": {
        "name": "Max-heap by negating",
        "explain": "`heapq` only ever gives you the smallest item. To get the largest, push `-x` and negate again when "
                   "you pop. With tuples, negate the field that should come out biggest first: `(-priority, ...)`.",
    },
    "heap.two_heaps": {
        "name": "Two heaps for the median",
        "explain": "Keep the smaller half of the numbers in a max-heap and the larger half in a min-heap, with every "
                   "value in the first no bigger than every value in the second, and the first one the same size or "
                   "one bigger. The median is the first heap's top, or the average of both tops.",
    },
    "heap.lazy_delete": {
        "name": "Lazy deletion",
        "explain": "A heap can't remove an item from the middle. Instead, mark it as gone (count it in a dict, or keep "
                   "a set of live entries) and leave it where it is. Whenever you look at the top, pop marked items "
                   "first. Each item is still pushed once and popped once.",
    },
    "heap.k_way_merge": {
        "name": "Merging sorted lists with a heap",
        "explain": "To take the smallest items from many sorted lists, put each list's first item in a min-heap "
                   "together with where it came from: `(value, which_list, position)`. Pop the smallest, then push "
                   "the next item from the same list. The heap holds at most one item per list.",
    },
```

- [ ] **Step 4: New teachers.** `course/3_data_structures/17_heaps/max_bag.py`:

```python
"""
Max With Removals                                                             [easy]

Keep a bag of numbers (repeats allowed):

    add(x)      put x in the bag
    remove(x)   take one copy of x out (x is always in the bag)
    max()       the largest number in the bag, or None if it's empty

Example:
    b = MaxBag()
    b.add(5); b.add(9); b.add(9)
    b.max()       ->  9
    b.remove(9)
    b.max()       ->  9       one 9 is still there
    b.remove(9)
    b.max()       ->  5

Aim for:  O(log n) per call. The last test makes 300,000 calls on a bag of up to
          150,000 numbers: max() over a list, or keeping a sorted list, is O(n) per
          call and times out.
Hint:     A heap can't delete from the middle, so don't. Keep a max-heap (push -x)
          and a Counter of numbers waiting to be removed: remove(x) just counts x.
          In max(), pop the top while it's waiting to be removed (counting it off),
          then read the top.
"""


class MaxBag:
    def __init__(self):
        raise NotImplementedError

    def add(self, x: int) -> None:
        raise NotImplementedError

    def remove(self, x: int) -> None:
        raise NotImplementedError

    def max(self) -> int | None:
        raise NotImplementedError


CLASS = "MaxBag"


def _big():
    import heapq
    import random
    from collections import Counter
    rng = random.Random(1705)
    heap, gone, present = [], Counter(), []
    ops, res = [("MaxBag",)], [None]

    def top():
        while heap and gone[-heap[0]]:
            gone[-heap[0]] -= 1
            heapq.heappop(heap)
        return -heap[0] if heap else None

    for step in range(300_000):
        r = rng.random()
        if step < 150_000 or r < 1 / 3 or not present:
            x = rng.randint(-10**6, 10**6)
            heapq.heappush(heap, -x)
            present.append(x)
            ops.append(("add", x))
            res.append(None)
        elif r < 2 / 3:
            i = rng.randrange(len(present))
            present[i], present[-1] = present[-1], present[i]
            x = present.pop()
            gone[x] += 1
            ops.append(("remove", x))
            res.append(None)
        else:
            ops.append(("max",))
            res.append(top())
    return ops, res


TEACHES = ["heap.lazy_delete"]
USES = ["heap.max_negate"]

TESTS = [
    ([("MaxBag",), ("add", 5), ("add", 9), ("add", 9), ("max",), ("remove", 9), ("max",), ("remove", 9), ("max",)],
     [None, None, None, None, 9, None, 9, None, 5]),
    ([("MaxBag",), ("max",), ("add", -3), ("max",), ("remove", -3), ("max",)], [None, None, None, -3, None, None]),
    ([("MaxBag",), ("add", 1), ("add", 7), ("add", 4), ("remove", 4), ("max",), ("remove", 7), ("max",), ("add", 2),
      ("max",)],
     [None, None, None, None, None, 7, None, 1, None, 2]),
    _big(),
]
```

  `solutions/max_bag.py`:

```python
import heapq
from collections import Counter


class MaxBag:
    # Lazy deletion: removals are only counted, and dead values are popped when they reach the top.
    def __init__(self):
        self.heap = []                      # negated: a max-heap
        self.gone = Counter()               # values removed but still inside the heap

    def add(self, x: int) -> None:
        heapq.heappush(self.heap, -x)

    def remove(self, x: int) -> None:
        self.gone[x] += 1

    def max(self) -> int | None:
        while self.heap and self.gone[-self.heap[0]]:
            self.gone[-self.heap[0]] -= 1
            heapq.heappop(self.heap)
        return -self.heap[0] if self.heap else None
```

  `course/3_data_structures/17_heaps/k_smallest_sums.py`:

```python
"""
Smallest Pair Sums                                                            [easy]

`a` and `b` are sorted. Every pair (a[i], b[j]) has the sum a[i] + b[j].
Return the k smallest of those sums, smallest first. 1 <= k <= len(a) * len(b).

Example:
    k_smallest_sums([1, 7, 11], [2, 4, 6], 3)  ->  [3, 5, 7]      1+2, 1+4 and 1+6

Aim for:  O(k log k). The last test has 100,000 numbers in each list and
          k = 100,000: building every sum means 10 billion pairs.
Hint:     Think of each a[i] as the start of its own sorted list: a[i] + b[0],
          a[i] + b[1], ... Put the first sum of each list (at most k of them) in
          a min-heap as (sum, i, j). Pop the smallest k times, and each time push
          the next sum from the same list, (i, j + 1).
"""


def k_smallest_sums(a: list[int], b: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _fast(a, b, k):
    import heapq
    heap = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    heapq.heapify(heap)
    out = []
    while len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append(s)
        if j + 1 < len(b):
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out


def _big():
    a, b = list(range(0, 200_000, 2)), list(range(0, 300_000, 3))
    return (a, b, 100_000), _fast(a, b, 100_000)


TEACHES = ["heap.k_way_merge"]
USES = []

TESTS = [
    (([1, 7, 11], [2, 4, 6], 3), [3, 5, 7]),
    (([1, 1, 2], [1, 2, 3], 2), [2, 2]),
    (([1, 2], [3], 2), [4, 5]),
    (([5], [5], 1), [10]),
    (([-3, 0, 4], [-1, 2], 6), [-4, -1, -1, 2, 3, 6]),
    (([1, 2, 3], [10, 20, 30], 9), [11, 12, 13, 21, 22, 23, 31, 32, 33]),
    _big(),
]
```

  `solutions/k_smallest_sums.py`:

```python
import heapq


def k_smallest_sums(a: list[int], b: list[int], k: int) -> list[int]:
    # Each a[i] heads a sorted list a[i] + b[0], a[i] + b[1], ...: a k-way merge. O(k log k).
    heap = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    heapq.heapify(heap)
    out = []
    while len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append(s)
        if j + 1 < len(b):                  # the next sum from the same list
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out
```

- [ ] **Step 5: Ranks.** `median_finder.py`'s header becomes `Find Median from Data Stream` padded to
  84 with `[easy]` (it was 86 wide). In `merge_k_sorted.py`, `[hard]` becomes `[medium]`, keeping 84.
- [ ] **Step 6: Tag.**

```bash
python $TAG course/3_data_structures/17_heaps push_keep_k=:heap.top_k last_stone=:heap.max_negate kth_largest_stream=heap.top_k median_finder=heap.max_negate:heap.two_heaps twitter=heap.max_negate,heap.k_way_merge k_closest=heap.top_k,heap.max_negate kth_largest=heap.top_k min_meeting_rooms=intervals.sort_by_start least_interval= merge_k_sorted=heap.k_way_merge min_interval_query=intervals.sort_by_start,heap.lazy_delete sliding_window_median=window.fixed,heap.max_negate,heap.two_heaps,heap.lazy_delete skyline=heap.max_negate,heap.lazy_delete task_scheduler=heap.max_negate,heap.lazy_delete
```

  Expected: 14 `tagged` lines.
- [ ] **Step 7: Run** the unit tests (all pass) and `--check 17_ coverage`. Expected: 16 `ok`; `65 techniques, 175 problem(s) not audited yet`.
- [ ] **Step 8: Commit** `Stage 3 audit: topic 17 tagged, with max_bag and k_smallest_sums` /
  `Lazy deletion and merging with a heap get basic problems; median_finder is now easy and teaches two heaps. merge_k_sorted is now a medium.`

### Task 8: Topic 18, tries

**Files:** `course/techniques.py` (2 entries); `18_tries/count_prefixes.py` (re-rank, big test); create
`18_tries/stream_matches.py` and its solution; every problem file (tags).

- [ ] **Step 1: Failing tests:**

```python
    def test_topic_18(self):
        self.assert_audited("18_tries")
        self.assert_teaches({"trie_insert": ["trie.walk"], "count_prefixes": ["trie.counts"]})
        self.assert_uses({"word_dictionary": ["recursion.trust", "trie.walk", "trie.counts"],
                          "stream_matches": ["trie.walk"], "palindrome_pairs": ["hash.complement"],
                          "autocomplete": ["bsearch.first_true"]})
        self.assertEqual(self.problems["count_prefixes"]["difficulty"], "easy")
        self.assertEqual(self.problems["stream_matches"]["difficulty"], "hard")

    def test_every_stage_3_topic_keeps_two_hard_problems(self):
        for topic_id in STAGE_3:
            hards = [n for n in self.items(topic_id) if self.problems[n]["difficulty"] == "hard"]
            self.assertGreaterEqual(len(hards), 2, (topic_id, hards))

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("daily_temperatures", lambda a, w: len(a[0]) >= 100_000 and w.count(0) >= 50_000)   # look ahead: O(n²)
        big("sliding_window_max", lambda a, w: len(a[0]) >= 100_000 and a[1] >= 50_000)          # max(): O(n * k)
        big("recently_used", lambda ops, w: len(ops) >= 200_000)                                 # list.remove: O(n)
        big("median_finder", lambda ops, w: len(ops) >= 150_000)                                 # insort: O(n)
        big("max_bag", lambda ops, w: len(ops) >= 300_000)                                       # max() or insort: O(n)
        big("k_smallest_sums", lambda a, w: min(len(a[0]), len(a[1]), a[2]) >= 100_000)          # k * k sums
        big("count_prefixes", lambda a, w: len(a[0]) >= 20_000 and len(a[1]) >= 20_000)          # scan every word
```

- [ ] **Step 2: Run** it. Expected: `test_topic_18` fails; the two-hards test fails on `18_tries`
  (only `palindrome_pairs`); the big-test check fails on `count_prefixes` (no big test yet).
- [ ] **Step 3: Registry:**

```python
    "trie.walk": {
        "name": "Walking a trie",
        "explain": "A trie stores words letter by letter in nested dicts: `node = node.setdefault(ch, {})` for each "
                   "letter, then mark the end, for example `node[\"$\"] = True`. Words that share a prefix share its "
                   "path, so looking up a word or a prefix takes O(its length).",
    },
    "trie.counts": {
        "name": "Counting words through a trie node",
        "explain": "Keep a count in every trie node and add 1 to it on each node a new word passes through. The number "
                   "of words that start with a prefix is then the count at the prefix's last node: walk down and read "
                   "it, O(length of the prefix).",
    },
```

- [ ] **Step 4: Re-rank `count_prefixes`.** `[medium]` becomes `  [easy]`. Replace the `Aim for:` line
  with `Aim for:  O(total letters in words + total letters in prefixes). The last test has 20,000`
  and `          words and 20,000 prefixes: scanning every word for every prefix times out.`.
  Add above `TESTS =`:

```python
def _big():
    import random
    rng = random.Random(1801)
    words = ["".join(rng.choice("abcde") for _ in range(rng.randint(3, 12))) for _ in range(20_000)]
    prefixes = ["".join(rng.choice("abcde") for _ in range(rng.randint(1, 6))) for _ in range(20_000)]
    counts = {}
    for w in words:
        for i in range(len(w) + 1):
            counts[w[:i]] = counts.get(w[:i], 0) + 1
    return (words, prefixes), [counts.get(p, 0) for p in prefixes]
```

  and end the `TESTS` list with `    _big(),`.
- [ ] **Step 5: New hard.** `course/3_data_structures/18_tries/stream_matches.py`:

```python
"""
Stream of Characters                                                          [hard]

Letters arrive one at a time. After each one, say whether the letters so far
END with one of the words: True if some word equals the last len(word) letters.

Example:
    stream_matches(["cd", "f", "kl"], "abcdefkl")
        ->  [False, False, False, True, False, True, False, True]
        "cd" ends at the 4th letter, "f" at the 6th and "kl" at the 8th.

Aim for:  well under O(len(letters) × number of words). The big test has 2,000
          words of up to 200 letters and 100,000 letters: comparing every word at
          every letter is far too slow.
Hint:     Put every word into a trie BACKWARDS. After each letter, walk the trie
          from that newest letter back through the stream: if you reach a node
          where a word ends, answer True; if the next letter isn't in the trie,
          stop.
"""


def stream_matches(words: list[str], letters: str) -> list[bool]:
    raise NotImplementedError  # replace this line with your solution


def _fast(words, letters):
    root = {}
    for w in words:
        node = root
        for ch in reversed(w):
            node = node.setdefault(ch, {})
        node["$"] = True
    out = []
    for i in range(len(letters)):
        node, j, hit = root, i, False
        while j >= 0 and letters[j] in node:
            node = node[letters[j]]
            if "$" in node:
                hit = True
                break
            j -= 1
        out.append(hit)
    return out


def _big():
    import random
    rng = random.Random(1801)
    words = ["".join(rng.choice("abcdefghij") for _ in range(rng.randint(3, 200))) for _ in range(2_000)]
    letters = "".join(rng.choice("abcdefghij") for _ in range(100_000))
    return (words, letters), _fast(words, letters)


USES = ["trie.walk"]

TESTS = [
    ((["cd", "f", "kl"], "abcdefkl"), [False, False, False, True, False, True, False, True]),
    ((["a"], "aba"), [True, False, True]),
    ((["ab", "b"], "ab"), [False, True]),
    ((["abc", "xbc"], "xbcabc"), [False, False, True, False, False, True]),
    (([], "ab"), [False, False]),
    ((["aaa"], "aaaa"), [False, False, True, True]),
    ((["x"], ""), []),
    _big(),
]
```

  `solutions/stream_matches.py`:

```python
def stream_matches(words: list[str], letters: str) -> list[bool]:
    # A trie of the words written backwards. Each new letter walks back through the
    # stream only while the trie still has a path, so most walks stop after a few steps.
    root = {}
    for w in words:
        node = root
        for ch in reversed(w):
            node = node.setdefault(ch, {})
        node["$"] = True                    # a whole word ends here
    out = []
    for i in range(len(letters)):
        node, j, hit = root, i, False
        while j >= 0 and letters[j] in node:
            node = node[letters[j]]
            if "$" in node:
                hit = True
                break
            j -= 1
        out.append(hit)
    return out
```

- [ ] **Step 6: Tag.**

```bash
python $TAG course/3_data_structures/18_tries trie_insert=:trie.walk autocomplete=bsearch.first_true count_prefixes=trie.walk:trie.counts implement_trie=trie.walk replace_words=trie.walk palindrome_pairs=hash.complement word_dictionary=recursion.trust,trie.walk,trie.counts
```

  Expected: 7 `tagged` lines.
- [ ] **Step 7: Run** the unit tests (all pass) and `--check 18_ coverage`.
  Expected: 8 `ok`; `67 techniques, 168 problem(s) not audited yet`.
- [ ] **Step 8: Commit** `Stage 3 audit: topic 18 tagged, with stream_matches` /
  `count_prefixes is now easy and teaches counts in trie nodes. stream_matches keeps two hards in Tries. Teacher big tests are checked against the naive solution.`

### Task 9: README, browser check and full verification

- [ ] **Step 1: README.** `400 coding exercises` becomes `406 coding exercises`.
- [ ] **Step 2: `tests/browser/stage_3.mjs`**, with the helpers and opening copied from `stage_2.mjs`. Checks, in order:
  1. `#/t/17_heaps`: the technique list equals `Keeping the k largest | Max-heap by negating | Two heaps for the median | Lazy deletion | Merging sorted lists with a heap`.
  2. Solve `push_keep_k` and `last_stone` (two checks).
  3. `#/p/median_finder`: `.tech-new h4` is `New technique: Two heaps for the median`.
  4. `#/p/sliding_window_median`: `.reveal-box` includes `This uses Two heaps for the median` and `Find Median from Data Stream teaches it`.
  5. Solve `median_finder`; then `sliding_window_median`'s `.reveal-box` includes `This uses Lazy deletion` and `Max With Removals teaches it`.
  6. `/api/reset-progress`, placement `skip`; solve `insert_after` and `reverse_between`; then
     `#/p/merge_two_lists`: `.tech-banner` includes `This uses One pointer per list` and `Is It a Subsequence?`.
  7. No console errors. That is 11 checks.
- [ ] **Step 3:** In `tests/browser/README.md`, after the `stage_2.mjs` line, add `    bash tests/browser/fresh.sh 8173 stage_3.mjs`.
- [ ] **Step 4: Run** `bash tests/browser/fresh.sh 8173 stage_3.mjs`. Expected: 11 of 11. If a list fails only
  on order, compare with `items` from `server.load_course()` and fix the expectation only if the ladder is right.
- [ ] **Step 5:** Earlier scenarios: `technique_coverage.mjs` (23), `stage_1.mjs` (14), `stage_2.mjs` (15), and
  the scratchpad's Phase 1 t4–t8 (54). Delete `tests/browser/technique_coverage.png` if it appears.
- [ ] **Step 6:** `python -m unittest discover -s tests` (all pass) and `python server.py --check`: 406 problems `ok`,
  `ok   starting check`, `67 techniques, 168 problem(s) not audited yet`, `All good.`
- [ ] **Step 7: Commit** `Stage 3 audit: README count and a browser check for topic 17's techniques`.
