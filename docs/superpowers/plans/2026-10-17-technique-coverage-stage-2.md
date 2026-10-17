# Technique coverage, Part 2 Stage 2: audit topics 06–11 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in topics 06–11 lists the techniques it uses. Each of those techniques is
taught by a basic problem that comes earlier, and no Stage 2 problem relies on a later topic.

**Architecture:** Content work only, no server change. 18 techniques join `course/techniques.py`
(45 in all). Every Stage 2 problem file gets `USES` (and `TEACHES` on teachers). Five new easy
teachers are added and two mediums are re-ranked to easy. Two heap problems move to the Heaps topic.
USES lists across the course are put in teaching order, and a course-wide test keeps them that
way. A `Stage2Audit` test class pins all of it.

**Tech Stack:** Python 3.12 stdlib, `unittest`, the existing `--check` self-check, and the Node
headless-Chrome scenarios in `tests/browser/`.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md` (Part 2: the content
audit, "What counts as a technique" and "Fixing a gap"). The Stage 1 plan,
`docs/superpowers/plans/2026-10-16-technique-coverage-stage-1.md`, is the model for this one.

## Global Constraints

- No new dependencies: no pip or npm packages.
- Problem names, topic ids and drill keys never change. Moving a file between topic folders is
  allowed; progress, saved code and study plans are keyed by name.
- `USES` and `TEACHES` go **after** the problem's function or class, directly above `TESTS =` or
  `STEPS =`. Assignments above the first `def` are copied into the starter code.
- `USES` lists techniques **in teaching order**: the order their teachers come in the course. The
  in-topic lock names the first unsolved teacher in `USES`.
- A teacher is a `snippet`, `guided` or `easy` problem. Every technique has exactly one teacher,
  and it comes before every problem that uses the technique.
- A technique from a later topic is never allowed. Cross-topic gaps are fixed in the earlier topic.
- Every topic keeps at least two hard problems (README: "at least two hard problems in every topic").
- Problem headers are 84 characters wide: the title, spaces, then `[easy]` (or another kind) at the end.
- Edits keep each file's own line endings (some course files are CRLF, some LF).
- A teacher's big test must time out (2 s per test, `runner/judge.py`) for the naive solution a
  learner without the technique would write.
- Tests: `python -m unittest discover -s tests` (one file: add `-p "test_x.py"`). Self-check:
  `python server.py --check <filters>`. A filter matches a problem name or a topic id; `coverage`
  runs the technique check.
- `TAG` below means `C:/Users/sam/AppData/Local/Temp/claude/C--Users-sam-Desktop-dsa/37698c59-d18f-494f-9d0b-cad64d5356c4/scratchpad/s2/tag.py`
  (created in Task 1, outside the repo).
- End every commit message with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Audit results

Read for every Stage 2 problem: statement, hint and reference solution. The rule from the spec's
"What counts as a technique" applies: `Counter`, `sorted` with a key, `bisect`, `deque` and
`heapq` used for what they plainly do are Python tools (topic 02 covers them), and a medium or
hard may keep one insight of its own ("own" in the table).

**New techniques (18), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `pointers.opposite_ends` | Pointers at both ends | `pointer_step` (snippet, 06) | reuse |
| `pointers.two_sequences` | One pointer per list | `merge_sorted` | **new** easy in 06: `merge_logs`, `min_window_subsequence` and `shortest_removal_to_sort` all walk two sequences with a pointer each |
| `window.fixed` | Fixed-size window | `slide_sum` (snippet, 07) | reuse |
| `window.variable` | Growing and shrinking a window | `longest_k_distinct` (guided, 07) | reuse |
| `window.shortest` | Shortest window | `min_subarray_len` | **re-rank** medium → easy: it is the plainest shortest-window problem, and `min_window` relies on it |
| `window.count` | Counting with a window | `nice_subarrays` | **new** easy in 07: the spec's "exactly k" gap (`subarrays_k_distinct`); `smallest_distance_pair` (09) counts pairs the same way |
| `prefix.sums` | Prefix sums | `prefix_sums` (snippet, 08) | reuse |
| `prefix.count_dict` | Counting earlier prefix sums | `zero_sum_subarrays` | **new** easy in 08: equal prefixes, the plainest form. `subarray_sum_equals_k` stays a medium and adds `total - k` |
| `prefix.difference` | Difference array | `range_additions` | **new** easy in 08: `min_moves_complementary` and `min_k_bit_flips` rely on it |
| `bsearch.first_true` | Binary search for the first yes | `lower_bound` (snippet, 09) | reuse |
| `bsearch.on_answer` | Binary search on the answer | `ship_capacity` (guided, 09) | reuse. Its check is the same greedy pass `split_array_largest_sum` needs, so that problem stays in 09 |
| `intervals.overlap` | Do two intervals overlap? | `overlaps` (snippet, 10) | reuse |
| `intervals.merge` | Absorbing an overlap | `insert_interval` (guided, 10) | reuse |
| `intervals.sort_by_start` | Sort by start, then compare neighbours | `can_attend_meetings` (easy, 10) | reuse |
| `intervals.earliest_end` | Earliest end first | `non_overlapping` | **re-rank** medium → easy: `pick_talks` (11) relies on it |
| `greedy.kadane` | Extend or restart | `extend_or_restart` (snippet, 11) | reuse |
| `greedy.farthest_reach` | Farthest reach | `min_jumps` (guided, 11) | reuse |
| `greedy.forced_first` | The forced first move | `min_suffix_flips` | **new** easy in 11: `hand_of_straights` and `min_k_bit_flips` both make the one move the leftmost item allows |

**Problems that rely on a later topic, moved to the topic of their last prerequisite** (Stage 3
tags them there):

| Problem | From | To | Needs |
|---|---|---|---|
| `min_meeting_rooms` | 10 | `17_heaps` | a min-heap of end times |
| `min_interval_query` | 10 | `17_heaps` | a heap of candidates, popping the ones that have ended |

Topic 10 keeps two hards (`summary_ranges`, `range_module`).

**Tags for every problem.** USES is written in teaching order.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 06 | `pointer_step` (snippet) | `pointers.opposite_ends` | | |
| 06 | `count_pairs_below` (guided) | | `pointers.opposite_ends` | own: count `right - left` pairs at once |
| 06 | `remove_duplicates_sorted` | | `array.write_pointer` | |
| 06 | `two_sum_sorted`, `valid_palindrome` | | `pointers.opposite_ends` | |
| 06 | `merge_sorted` (new) | `pointers.two_sequences` | | |
| 06 | `three_sum` | | `pointers.opposite_ends` | own: fix one number, skip equal neighbours |
| 06 | `container_with_most_water` | | `pointers.opposite_ends` | own: move the shorter line |
| 06 | `min_window_subsequence` (hard) | | `pointers.two_sequences` | own: walk back from the end for the latest start |
| 06 | `shortest_removal_to_sort` (hard) | | `pointers.two_sequences` | own: keep a sorted prefix and a sorted suffix |
| 06 | `trap_rain_water` (hard) | | `array.left_right_passes`, `pointers.opposite_ends` | own: settle the side with the smaller max |
| 06 | `merge_logs` (build) | | `pointers.two_sequences` | |
| 07 | `slide_sum` (snippet) | `window.fixed` | | |
| 07 | `longest_k_distinct` (guided) | `window.variable` | | |
| 07 | `max_sum_subarray_k`, `check_inclusion` | | `window.fixed` | |
| 07 | `min_subarray_len` (now easy) | `window.shortest` | `window.variable` | |
| 07 | `nice_subarrays` (new) | `window.count` | `window.variable` | |
| 07 | `character_replacement` | | `window.variable` | own: length minus the top count must be ≤ k |
| 07 | `longest_unique_substring` | | `window.variable` | own: jump left past the last copy |
| 07 | `min_ops_continuous` (hard) | | `window.variable` | own: slide over the sorted distinct values |
| 07 | `min_window` (hard) | | `window.variable`, `window.shortest` | own: count what's still missing |
| 07 | `subarrays_k_distinct` (hard) | | `window.variable`, `window.count` | |
| 07 | `concat_all_words` (hard) | | `window.variable` | own: one window per offset |
| 07 | `rate_limiter` (build) | | `window.variable` | `deque` is a toolkit tool |
| 08 | `prefix_sums` (snippet) | `prefix.sums` | | |
| 08 | `range_sum_queries` (guided), `range_sums`, `score_board` (build) | | `prefix.sums` | |
| 08 | `pivot_index` | | `prefix.sums` | own: right side = total − left − x |
| 08 | `zero_sum_subarrays` (new) | `prefix.count_dict` | `hash.count_pairs`, `prefix.sums` | |
| 08 | `range_additions` (new) | `prefix.difference` | `prefix.sums` | |
| 08 | `subarray_sum_equals_k` | | `hash.complement`, `prefix.sums`, `prefix.count_dict` | |
| 08 | `count_subarrays_median_k` (hard) | | `prefix.sums`, `prefix.count_dict` | own: +1 / −1 balances around k |
| 08 | `max_sum_three_subarrays` (hard) | | `scan.best_so_far`, `array.left_right_passes`, `prefix.sums` | own: try every middle window |
| 08 | `min_moves_complementary` (hard) | | `prefix.sums`, `prefix.difference` | own: each pair costs 0, 1 or 2 per target |
| 08 | `submatrix_sum_target` (hard) | | `prefix.sums`, `prefix.count_dict` | own: squash the rows between two rows |
| 09 | `lower_bound` (snippet) | `bsearch.first_true` | | |
| 09 | `ship_capacity` (guided) | `bsearch.on_answer` | `bsearch.first_true` | |
| 09 | `binary_search`, `search_insert`, `time_map` (build) | | `bsearch.first_true` | |
| 09 | `sqrt_floor`, `min_eating_speed`, `split_array_largest_sum` (hard) | | `bsearch.first_true`, `bsearch.on_answer` | |
| 09 | `find_min_rotated` | | `bsearch.first_true` | own: compare with the last element |
| 09 | `search_matrix` | | `bsearch.first_true` | own: index k is `matrix[k // n][k % n]` |
| 09 | `search_rotated` | | `bsearch.first_true` | own: one half is always sorted |
| 09 | `median_two_sorted` (hard) | | `bsearch.first_true` | own: binary search the cut |
| 09 | `smallest_distance_pair` (hard) | | `window.variable`, `window.count`, `bsearch.first_true`, `bsearch.on_answer` | |
| 10 | `overlaps` (snippet) | `intervals.overlap` | | |
| 10 | `insert_interval` (guided) | `intervals.merge` | `intervals.overlap` | |
| 10 | `can_attend_meetings` | `intervals.sort_by_start` | `intervals.overlap` | |
| 10 | `non_overlapping` (now easy) | `intervals.earliest_end` | `intervals.overlap` | |
| 10 | `largest_number` | | | own: compare a + b with b + a |
| 10 | `merge_intervals`, `free_slots` (build) | | `intervals.overlap`, `intervals.merge`, `intervals.sort_by_start` | `free_slots` own: the gaps between blocks |
| 10 | `summary_ranges` (hard) | | `bsearch.first_true`, `intervals.merge` | own: the four cases for a new value |
| 10 | `range_module` (hard) | | `bsearch.first_true`, `intervals.overlap`, `intervals.merge` | own: keep the pieces sticking out |
| 11 | `extend_or_restart` (snippet) | `greedy.kadane` | | |
| 11 | `min_jumps` (guided) | `greedy.farthest_reach` | | |
| 11 | `min_suffix_flips` (new) | `greedy.forced_first` | | |
| 11 | `gas_station`, `max_subarray` | | `greedy.kadane` | `gas_station` own: enough gas in total means the last restart works |
| 11 | `can_jump`, `partition_labels`, `min_taps` (hard) | | `greedy.farthest_reach` | own: stretch to each letter's last index; turn taps into a reach per left point |
| 11 | `hand_of_straights` | | `greedy.forced_first` | |
| 11 | `merge_triplets`, `valid_paren_string`, `patching_array` (hard) | | | own: drop triplets that overshoot; a range of open counts; patching `reach` doubles it |
| 11 | `candy` (hard) | | `array.left_right_passes` | own: take the max of both passes |
| 11 | `min_k_bit_flips` (hard) | | `prefix.difference`, `greedy.forced_first` | |
| 11 | `pick_talks` (build) | | `intervals.earliest_end` | |

**Teaching order across the course.** The Graph traversal pilot and five Stage 1 problems list USES
newest first. When two same-topic teachers are both unsolved, the lock can then name the later one.
Task 1 reorders those 18 lists and adds a course-wide test.

**Known limit.** `merge_sorted` can be passed with `sorted(a + b)`, which is O(n log n), not naive.
Its big test rejects the O(n · m) insertion approach. The statement asks for no `sorted()`.

## Review Focus

1. **Moved problems keep their history.** `min_meeting_rooms` and `min_interval_query` keep their
   progress and study-plan entries in Heaps. Owners: the Task 1 test
   `test_problems_moved_to_the_topic_of_their_last_prerequisite`, and the existing
   `test_every_plan_item_exists`.
2. **The lock names the right basic problem.** When a problem uses two unsolved teachers, the lock
   names the earlier one. Owners: the Task 1 test `test_uses_are_in_teaching_order`, and the Task 8
   browser check on `min_k_bit_flips`.
3. **A teacher can't be passed without its technique.** Solving a teacher marks the technique
   learned. Owner: the Task 7 test `test_teacher_big_tests_reject_the_naive_solution` (5 new and 2
   re-ranked teachers). Every naive version below was timed at over 6 s while this plan was written.
4. **Re-ranking and moving keep two hards in every Stage 2 topic.** Owner: the Task 6 test
   `test_every_stage_2_topic_keeps_two_hard_problems`.
5. **Tags never leak into a starter.** Owner: the existing course-wide `test_tags_stay_out_of_starters`.

---

### Task 1: Teaching order, the moves and the test base

**Files:**
- Modify: `tests/test_coverage.py` (`AuditBase`, `Stage1Audit`, new `Stage2Audit`, `RealCourse`)
- Modify: the USES line in the 18 files listed by Step 2's output
- Move: `course/2_core_patterns/10_sorting_and_intervals/min_meeting_rooms.py` and
  `min_interval_query.py` → `course/3_data_structures/17_heaps/`
- Modify: `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`
- Create: `TAG` (outside the repo)

**Interfaces:**
- Produces: `AuditBase(unittest.TestCase)` with `setUpClass`, `items(topic_id)`,
  `assert_audited(topic_id)`, `assert_uses({name: [ids]})` (sets), `assert_teaches({name: [ids]})`
  (lists) and `cases_of(name)`, all moved unchanged from `Stage1Audit`. `Stage1Audit` and
  `Stage2Audit` both subclass it. Tasks 2–7 add test methods to `Stage2Audit`.
- Produces: `TAG FOLDER NAME=USES[:TEACHES] ...`, the same tool as Stage 1 (its code is in the
  Stage 1 plan, Task 1 Step 6).

- [ ] **Step 1: Write the failing tests.** In `tests/test_coverage.py`, split `Stage1Audit`: a new
  `class AuditBase(unittest.TestCase)` gets its `setUpClass` and the helpers (`items`,
  `assert_audited`, `assert_uses`, `assert_teaches`, `cases_of`), and `Stage1Audit(AuditBase)`
  keeps only its `test_` methods. Add to `RealCourse`:

```python
    def test_uses_are_in_teaching_order(self):
        # The in-topic lock names the first unsolved teacher in USES, so USES follows course order.
        topics, problems = server.load_course()
        pos = {n: i for i, n in enumerate(n for t in topics for n in t["items"])}
        teacher = {t: n for n, p in problems.items() for t in p["teaches"]}
        wrong = [n for n, p in problems.items() if p["uses"] != sorted(p["uses"], key=lambda t: pos[teacher[t]])]
        self.assertEqual(wrong, [])
```

  Then, above `if __name__ == "__main__":`:

```python
STAGE_2 = ("06_two_pointers", "07_sliding_window", "08_prefix_sums", "09_binary_search",
           "10_sorting_and_intervals", "11_greedy")


class Stage2Audit(AuditBase):
    """Part 2, Stage 2: topics 06-11 fully audited (docs/superpowers/plans/2026-10-17-technique-coverage-stage-2.md)."""

    def test_problems_moved_to_the_topic_of_their_last_prerequisite(self):
        for name in ("min_meeting_rooms", "min_interval_query"):
            self.assertEqual(self.problems[name]["topic_id"], "17_heaps", name)
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected: two
  failures. `test_uses_are_in_teaching_order` lists 18 problems: `max_chunks_to_sorted`,
  `grid_illumination`, `calculate`, `count_of_atoms`, `scramble_string` and 13 in Graph traversal.
  The move test reports `10_sorting_and_intervals`.

- [ ] **Step 3: Reorder the USES lines.** Run this from the repo root:

```python
import json, re, server
topics, problems = server.load_course()
pos = {n: i for i, n in enumerate(n for t in topics for n in t["items"])}
teacher = {t: n for n, p in problems.items() for t in p["teaches"]}
for name, p in problems.items():
    want = sorted(p["uses"], key=lambda t: pos[teacher[t]])
    if p["uses"] != want:
        path = next(server.COURSE.glob(f"*/*/{name}.py"))
        text = path.read_bytes().decode("utf-8")
        new = re.sub(r"^USES = \[[^\]\n]*\]", "USES = " + json.dumps(want), text, count=1, flags=re.M)
        path.write_bytes(new.encode("utf-8"))
        print("reordered", name)
```

  Expected: 18 `reordered` lines. `git diff --stat` shows 18 files with one line changed each.

- [ ] **Step 4: Move the two heap problems.**

```bash
git mv course/2_core_patterns/10_sorting_and_intervals/min_meeting_rooms.py course/3_data_structures/17_heaps/min_meeting_rooms.py
git mv course/2_core_patterns/10_sorting_and_intervals/min_interval_query.py course/3_data_structures/17_heaps/min_interval_query.py
```

- [ ] **Step 5: Update the spec.** In `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`:
  - Row `` | 07 Sliding window | "exactly k" = at-most-k minus at-most-(k − 1) | `subarrays_k_distinct` | ``:
    the last cell becomes `` `subarrays_k_distinct` (fixed: the new `nice_subarrays` teaches it) ``.
  - Row `` | `min_k_bit_flips` (03) | a queue of where flips end | 13 Queues | `` becomes
    `` | `min_k_bit_flips` (03) | the forced first flip, and a difference array for where flips end | 08 and 11 (fixed: moved to 11) | ``.
  - Rows for `concat_all_words`, `submatrix_sum_target` and `min_meeting_rooms`, `min_interval_query`:
    add ` (fixed: moved there)` to the last cell.
  - Row `split_array_largest_sum`: the last cell becomes
    `` 11 Greedy (fixed: `ship_capacity`, 09's guided problem, already teaches the same check) ``.
  - After the bullet that starts `- Every problem gets \`USES\``, add:
    `- \`USES\` lists techniques in teaching order, the order their teachers come in the course, so the lock names the first basic problem to do.`
    (wrapped at 100 characters like its neighbours).

- [ ] **Step 6: The tagging helper.** Create `TAG` with the code from the Stage 1 plan, Task 1 Step 6.

- [ ] **Step 7: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: Run** `python server.py --check min_meeting_rooms min_interval_query coverage`.
  Expected: two `ok` lines under topic 17; `ok   technique coverage … 27 techniques, 317 problem(s)
  not audited yet`; `All good.`

- [ ] **Step 9: Commit**

```bash
git add tests/test_coverage.py course docs/superpowers/specs/2026-10-16-technique-coverage-design.md
git commit -m "Stage 2 audit setup: USES in teaching order, two heap problems moved to Heaps" -m "The in-topic lock names the first unsolved teacher in USES, so USES now follows course order everywhere, with a test. min_meeting_rooms and min_interval_query need heaps and move to topic 17." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Topic 06, two pointers

**Files:**
- Modify: `course/techniques.py` (2 entries)
- Create: `course/2_core_patterns/06_two_pointers/merge_sorted.py`, `solutions/merge_sorted.py`
- Modify: every other problem file in `06_two_pointers/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `AuditBase`, `Stage2Audit`, `TAG` (Task 1); `array.write_pointer`,
  `array.left_right_passes` (Stage 1).
- Produces: `pointers.opposite_ends`, `pointers.two_sequences`.

- [ ] **Step 1: Write the failing test.** Add to `Stage2Audit`:

```python
    def test_topic_06(self):
        self.assert_audited("06_two_pointers")
        self.assert_teaches({"pointer_step": ["pointers.opposite_ends"], "merge_sorted": ["pointers.two_sequences"]})
        self.assert_uses({"remove_duplicates_sorted": ["array.write_pointer"],
                          "trap_rain_water": ["array.left_right_passes", "pointers.opposite_ends"],
                          "min_window_subsequence": ["pointers.two_sequences"],
                          "merge_logs": ["pointers.two_sequences"], "count_pairs_below": ["pointers.opposite_ends"]})
        self.assertEqual(self.problems["merge_sorted"]["difficulty"], "easy")
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_06` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "pointers.opposite_ends": {
        "name": "Pointers at both ends",
        "explain": "Put `left` at the start and `right` at the end, and move them towards each other. On a sorted "
                   "list, a pair sum that's too small means nums[left] can't work with anything left, so move left "
                   "up; too big means move right down. Each step rules out one item for good: O(n) instead of "
                   "trying every pair.",
    },
    "pointers.two_sequences": {
        "name": "One pointer per list",
        "explain": "To walk two sequences together, keep an index into each. Each step compares `a[i]` with `b[j]` "
                   "and moves one of them on, or both: merging takes the smaller, and matching a subsequence moves "
                   "j only on a match. Neither pointer ever goes back, so it's O(len(a) + len(b)).",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/2_core_patterns/06_two_pointers/merge_sorted.py`:

```python
"""
Merge Two Sorted Lists                                                        [easy]

`a` and `b` are both sorted. Return one sorted list that holds every number
from both.

Example:
    merge_sorted([1, 4, 9], [2, 3, 10])  ->  [1, 2, 3, 4, 9, 10]

Aim for:  O(len(a) + len(b)): walk each list once. Don't call sorted(): the point
          is to use the order the lists already have.
Hint:     Keep i in a and j in b. While both have numbers left, append the smaller
          of a[i] and b[j] and move that pointer on. When one list runs out, add
          the rest of the other.
"""


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["pointers.two_sequences"]
USES = []

TESTS = [
    (([1, 4, 9], [2, 3, 10]), [1, 2, 3, 4, 9, 10]),
    (([], [1, 2]), [1, 2]),
    (([5], []), [5]),
    (([], []), []),
    (([1, 1, 3], [1, 2]), [1, 1, 1, 2, 3]),
    (([-3, 0], [-5, -4, 7]), [-5, -4, -3, 0, 7]),
    (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
    ((list(range(0, 400_000, 2)), list(range(1, 400_000, 2))), list(range(400_000))),
]
```

  Create `solutions/merge_sorted.py`:

```python
def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    # One pointer per list; each step takes the smaller front. O(len(a) + len(b)).
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]              # one of these is empty
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/2_core_patterns/06_two_pointers pointer_step=:pointers.opposite_ends count_pairs_below=pointers.opposite_ends remove_duplicates_sorted=array.write_pointer two_sum_sorted=pointers.opposite_ends valid_palindrome=pointers.opposite_ends three_sum=pointers.opposite_ends container_with_most_water=pointers.opposite_ends min_window_subsequence=pointers.two_sequences shortest_removal_to_sort=pointers.two_sequences trap_rain_water=array.left_right_passes,pointers.opposite_ends merge_logs=pointers.two_sequences
```

  Expected: 11 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 06_ coverage`. Expected: 12 `ok` lines;
  `ok   technique coverage … 29 techniques, 306 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 2 audit: topic 06 tagged, with merge_sorted" -m "One pointer per list gets a basic problem before merge_logs, min_window_subsequence and shortest_removal_to_sort rely on it." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: Topic 07, sliding window

**Files:**
- Modify: `course/techniques.py` (4 entries)
- Create: `course/2_core_patterns/07_sliding_window/nice_subarrays.py`, `solutions/nice_subarrays.py`
- Modify: `course/2_core_patterns/07_sliding_window/min_subarray_len.py` (re-rank, big test), every
  other problem file in `07_sliding_window/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage2Audit`, `TAG` (Task 1).
- Produces: `window.fixed`, `window.variable`, `window.shortest`, `window.count` (Task 5 uses the
  last two); the titles "Shortest Subarray With Sum at Least Target" and "Subarrays With k Odd
  Numbers" and the technique names, which Task 8's browser check reads.

- [ ] **Step 1: Write the failing test.** Add to `Stage2Audit`:

```python
    def test_topic_07(self):
        self.assert_audited("07_sliding_window")
        self.assert_teaches({"slide_sum": ["window.fixed"], "longest_k_distinct": ["window.variable"],
                             "min_subarray_len": ["window.shortest"], "nice_subarrays": ["window.count"]})
        self.assert_uses({"check_inclusion": ["window.fixed"], "min_window": ["window.variable", "window.shortest"],
                          "subarrays_k_distinct": ["window.variable", "window.count"],
                          "concat_all_words": ["window.variable"], "rate_limiter": ["window.variable"]})
        for name in ("min_subarray_len", "nice_subarrays"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_07` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "window.fixed": {
        "name": "Fixed-size window",
        "explain": "When a window of k items slides one step right, one item enters (`nums[right]`) and one leaves "
                   "(`nums[right - k]`). Update the sum or the counts with just those two: O(1) per step instead "
                   "of O(k).",
    },
    "window.variable": {
        "name": "Growing and shrinking a window",
        "explain": "Move `right` one step at a time to grow the window. Whenever it breaks the rule (too many kinds, "
                   "too big a sum), move `left` forward until it's fine again, undoing what leaves. Each index "
                   "enters once and leaves once, so it's O(n). For the longest good window, record its size after "
                   "shrinking.",
    },
    "window.shortest": {
        "name": "Shortest window",
        "explain": "For the SHORTEST window that works, grow `right` until the window is good. Then, while it's "
                   "still good, record its length and shrink from the left. The longest-window version shrinks "
                   "while the window is broken; this one shrinks while it works.",
    },
    "window.count": {
        "name": "Counting with a window",
        "explain": "To count windows instead of finding the best one: once [left, right] is good, every start from "
                   "left to right is good for this end too, so add `right - left + 1`. \"Exactly k\" can't be "
                   "shrunk towards this way, but \"at most k\" can, so exactly(k) = at_most(k) - at_most(k - 1).",
    },
```

- [ ] **Step 4: Re-rank `min_subarray_len`.** In `min_subarray_len.py` (LF line endings):
  - Header: replace `[medium]` with `  [easy]` (the line stays 84 wide).
  - Replace the line `Aim for:  O(n)` with the two lines
    `Aim for:  O(n). The last test has 100,000 numbers: trying every start is O(n²)` and
    `          and times out.`
  - Add `    ((50_000, [1] * 100_000), 50_000),` as the last entry of `TESTS`.

- [ ] **Step 5: The new teacher.** Create `course/2_core_patterns/07_sliding_window/nice_subarrays.py`:

```python
"""
Subarrays With k Odd Numbers                                                  [easy]

Count the contiguous subarrays of `nums` that hold exactly k odd numbers.
1 <= k <= len(nums).

Example:
    nice_subarrays([1, 1, 2, 1, 1], 3)  ->  2      [1, 1, 2, 1] and [1, 2, 1, 1]
    nice_subarrays([2, 4, 6], 1)        ->  0

Aim for:  O(n). The last test has 100,000 numbers: trying every start and end is
          O(n²) and times out.
Hint:     "At most k odd numbers" is easy with a window: for each right end, move
          left until the window holds at most k odds. Then every start from left
          to right works, so add right - left + 1. Exactly k is at_most(k) minus
          at_most(k - 1).
"""


def nice_subarrays(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["window.count"]
USES = ["window.variable"]

TESTS = [
    (([1, 1, 2, 1, 1], 3), 2),
    (([2, 4, 6], 1), 0),
    (([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2), 16),
    (([1], 1), 1),
    (([1, 1, 1], 1), 3),
    (([1, 1, 1], 3), 1),
    (([2, 1, 2], 1), 4),
    (([1 if i % 1000 == 0 else 2 for i in range(100_000)], 50), 50_001_000),
]
```

  Create `solutions/nice_subarrays.py`:

```python
def nice_subarrays(nums: list[int], k: int) -> int:
    def at_most(k):
        # For each right end, shrink until at most k odds; then every start in [left, right] works.
        left = odds = total = 0
        for right, x in enumerate(nums):
            odds += x % 2
            while odds > k:
                odds -= nums[left] % 2
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)      # exactly k = at most k minus at most k - 1
```

- [ ] **Step 6: Tag.**

```bash
python $TAG course/2_core_patterns/07_sliding_window slide_sum=:window.fixed longest_k_distinct=:window.variable max_sum_subarray_k=window.fixed min_subarray_len=window.variable:window.shortest character_replacement=window.variable longest_unique_substring=window.variable check_inclusion=window.fixed min_ops_continuous=window.variable min_window=window.variable,window.shortest subarrays_k_distinct=window.variable,window.count concat_all_words=window.variable rate_limiter=window.variable
```

  Expected: 12 `tagged` lines.

- [ ] **Step 7: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: Run** `python server.py --check 07_ coverage`. Expected: 13 `ok` lines;
  `ok   technique coverage … 33 techniques, 294 problem(s) not audited yet`; `All good.`

- [ ] **Step 9: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 2 audit: topic 07 tagged, with nice_subarrays" -m "Counting with a window, including exactly k = at most k minus at most k - 1, gets a basic problem before subarrays_k_distinct. min_subarray_len is now easy and teaches the shortest window." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: Topic 08, prefix sums

**Files:**
- Modify: `course/techniques.py` (3 entries)
- Create: `course/2_core_patterns/08_prefix_sums/zero_sum_subarrays.py`, `solutions/zero_sum_subarrays.py`
- Create: `course/2_core_patterns/08_prefix_sums/range_additions.py`, `solutions/range_additions.py`
- Modify: every other problem file in `08_prefix_sums/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage2Audit`, `TAG` (Task 1); `hash.count_pairs`, `hash.complement`,
  `scan.best_so_far`, `array.left_right_passes` (Stage 1).
- Produces: `prefix.sums`, `prefix.count_dict`, `prefix.difference` (Task 7 uses the last).

- [ ] **Step 1: Write the failing test.** Add to `Stage2Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_08` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "prefix.sums": {
        "name": "Prefix sums",
        "explain": "Build P with `P[0] = 0` and `P[k + 1] = P[k] + nums[k]`, so P[k] is the sum of the first k "
                   "numbers. Then the sum of nums[i..j] is `P[j + 1] - P[i]`: one subtraction instead of a loop.",
    },
    "prefix.count_dict": {
        "name": "Counting earlier prefix sums",
        "explain": "nums[i:j] adds up to k exactly when P[j] - P[i] == k. So walk once with a running total and a "
                   "dict counting the totals seen so far, starting with `{0: 1}` for the empty start, and at each "
                   "step add how many earlier totals equal `total - k`. Unlike a sliding window, this works with "
                   "negative numbers.",
    },
    "prefix.difference": {
        "name": "Difference array",
        "explain": "To add v to every index from l to r, touch only the ends: `diff[l] += v` and "
                   "`diff[r + 1] -= v`. After all the updates, a running total of diff gives each index's value. "
                   "Each update is O(1), and one pass at the end does the rest.",
    },
```

- [ ] **Step 4: The new teachers.** Create `course/2_core_patterns/08_prefix_sums/zero_sum_subarrays.py`:

```python
"""
Count Zero-Sum Subarrays                                                      [easy]

Count the contiguous subarrays of `nums` that add up to 0. Numbers can be
negative.

Example:
    zero_sum_subarrays([1, -1, 2, -2])  ->  3      [1, -1], [2, -2] and [1, -1, 2, -2]
    zero_sum_subarrays([0, 0])          ->  3

Aim for:  O(n). The last test has 100,000 numbers: adding up every subarray is
          O(n²) and times out.
Hint:     nums[i:j] adds up to 0 exactly when the running totals before i and
          before j are equal. So walk once with a running total and a dict of how
          many times each total has appeared, starting with {0: 1} for the empty
          start. A new total pairs with every earlier copy of itself.
"""


def zero_sum_subarrays(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["prefix.count_dict"]
USES = ["hash.count_pairs", "prefix.sums"]

TESTS = [
    (([1, -1, 2, -2],), 3),
    (([0, 0],), 3),
    (([1, 2, 3],), 0),
    (([],), 0),
    (([0],), 1),
    (([3, -3, 3, -3],), 4),
    (([4, 2, -3, 1, 6],), 1),
    (([1, -1] * 50_000,), 2_500_000_000),
]
```

  Create `solutions/zero_sum_subarrays.py`:

```python
def zero_sum_subarrays(nums: list[int]) -> int:
    # Equal running totals mark a zero-sum subarray between them. Count earlier copies. O(n).
    seen = {0: 1}                           # the empty start
    total = count = 0
    for x in nums:
        total += x
        count += seen.get(total, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
```

  Create `course/2_core_patterns/08_prefix_sums/range_additions.py`:

```python
"""
Range Additions                                                               [easy]

Start with n zeros. Each update [l, r, v] adds v to every index from l to r,
both ends included. Return the list after all the updates.

Example:
    range_additions(5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]])  ->  [-2, 0, 3, 5, 3]

Aim for:  O(n + updates). The last test has 100,000 indexes and 50,000 updates
          that each cover much of the list: adding v one index at a time times out.
Hint:     Keep a list diff of n + 1 zeros. An update only touches its two ends:
          diff[l] += v and diff[r + 1] -= v. At the end, the running total of diff
          up to each index is that index's value.
"""


def range_additions(n: int, updates: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["prefix.difference"]
USES = ["prefix.sums"]

TESTS = [
    ((5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]]), [-2, 0, 3, 5, 3]),
    ((3, []), [0, 0, 0]),
    ((1, [[0, 0, 7]]), [7]),
    ((4, [[0, 3, 1], [0, 3, 1]]), [2, 2, 2, 2]),
    ((6, [[2, 2, 5], [0, 5, -1], [3, 5, 4]]), [-1, -1, 4, 3, 3, 3]),
    ((100_000, [[i, 99_999 - i, 1] for i in range(50_000)]), [min(i, 99_999 - i) + 1 for i in range(100_000)]),
]
```

  Create `solutions/range_additions.py`:

```python
def range_additions(n: int, updates: list[list[int]]) -> list[int]:
    # Mark where each update starts and stops; a running total spreads it. O(n + updates).
    diff = [0] * (n + 1)
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v
    out, running = [], 0
    for i in range(n):
        running += diff[i]
        out.append(running)
    return out
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/2_core_patterns/08_prefix_sums prefix_sums=:prefix.sums range_sum_queries=prefix.sums pivot_index=prefix.sums range_sums=prefix.sums subarray_sum_equals_k=hash.complement,prefix.sums,prefix.count_dict count_subarrays_median_k=prefix.sums,prefix.count_dict max_sum_three_subarrays=scan.best_so_far,array.left_right_passes,prefix.sums min_moves_complementary=prefix.sums,prefix.difference submatrix_sum_target=prefix.sums,prefix.count_dict score_board=prefix.sums
```

  Expected: 10 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 08_ coverage`. Expected: 12 `ok` lines;
  `ok   technique coverage … 36 techniques, 284 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 2 audit: topic 08 tagged, with zero_sum_subarrays and range_additions" -m "Counting earlier prefix sums and the difference array get basic problems before subarray_sum_equals_k, submatrix_sum_target and min_moves_complementary rely on them." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Topic 09, binary search

**Files:**
- Modify: `course/techniques.py` (2 entries)
- Modify: every problem file in `09_binary_search/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage2Audit`, `TAG` (Task 1); `window.variable`, `window.count` (Task 3).
- Produces: `bsearch.first_true`, `bsearch.on_answer` (Task 6 uses the first).

- [ ] **Step 1: Write the failing test.** Add to `Stage2Audit`:

```python
    def test_topic_09(self):
        self.assert_audited("09_binary_search")
        self.assert_teaches({"lower_bound": ["bsearch.first_true"], "ship_capacity": ["bsearch.on_answer"]})
        self.assert_uses({"split_array_largest_sum": ["bsearch.first_true", "bsearch.on_answer"],
                          "smallest_distance_pair": ["window.variable", "window.count", "bsearch.first_true",
                                                     "bsearch.on_answer"],
                          "sqrt_floor": ["bsearch.first_true", "bsearch.on_answer"],
                          "median_two_sorted": ["bsearch.first_true"], "time_map": ["bsearch.first_true"]})
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_09` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "bsearch.first_true": {
        "name": "Binary search for the first yes",
        "explain": "Binary search keeps a range that must hold the answer and halves it each step, so it's O(log n). "
                   "The most reusable form finds the first index where a yes/no question turns yes, such as the "
                   "first `nums[i] >= x`: `lo, hi = 0, len(nums)`, then while lo < hi, set `hi = mid` on yes and "
                   "`lo = mid + 1` on no.",
    },
    "bsearch.on_answer": {
        "name": "Binary search on the answer",
        "explain": "When the answer is a number and \"does c work?\" flips from no to yes once as c grows, binary "
                   "search over c itself, between the smallest and the largest possible answer. Write the check as "
                   "its own function. It's often one greedy pass, such as filling each day until the next item "
                   "won't fit.",
    },
```

- [ ] **Step 4: Tag.**

```bash
python $TAG course/2_core_patterns/09_binary_search lower_bound=:bsearch.first_true ship_capacity=bsearch.first_true:bsearch.on_answer binary_search=bsearch.first_true sqrt_floor=bsearch.first_true,bsearch.on_answer search_insert=bsearch.first_true find_min_rotated=bsearch.first_true min_eating_speed=bsearch.first_true,bsearch.on_answer search_matrix=bsearch.first_true search_rotated=bsearch.first_true smallest_distance_pair=window.variable,window.count,bsearch.first_true,bsearch.on_answer median_two_sorted=bsearch.first_true split_array_largest_sum=bsearch.first_true,bsearch.on_answer time_map=bsearch.first_true
```

  Expected: 13 `tagged` lines.

- [ ] **Step 5: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 6: Run** `python server.py --check 09_ coverage`. Expected: 13 `ok` lines;
  `ok   technique coverage … 38 techniques, 271 problem(s) not audited yet`; `All good.`

- [ ] **Step 7: Commit**

```bash
git add course tests/test_coverage.py
git commit -m "Stage 2 audit: topic 09 tagged" -m "ship_capacity already teaches the greedy check split_array_largest_sum needs, so it stays in Binary search." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: Topic 10, sorting and intervals

**Files:**
- Modify: `course/techniques.py` (4 entries)
- Modify: `course/2_core_patterns/10_sorting_and_intervals/non_overlapping.py` (re-rank, big test),
  every other problem file in `10_sorting_and_intervals/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage2Audit`, `TAG` (Task 1); `bsearch.first_true` (Task 5).
- Produces: `intervals.overlap`, `intervals.merge`, `intervals.sort_by_start`,
  `intervals.earliest_end` (Task 7 uses the last); the technique names, which Task 8 reads.

- [ ] **Step 1: Write the failing tests.** Add to `Stage2Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_10` fails on unaudited problems; the two-hards test passes already and guards the move.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "intervals.overlap": {
        "name": "Do two intervals overlap?",
        "explain": "[a, b] and [c, d] overlap when `a <= d and c <= b`. It's easier to see the other way round: "
                   "they don't overlap when one ends before the other starts. Use `<` instead of `<=` when "
                   "touching shouldn't count.",
    },
    "intervals.merge": {
        "name": "Absorbing an overlap",
        "explain": "When an interval overlaps the one you're building, swallow it: `start = min(start, s)` and "
                   "`end = max(end, e)`. The max matters, because [1, 10] swallows [2, 3]. Intervals that don't "
                   "overlap are copied as they are.",
    },
    "intervals.sort_by_start": {
        "name": "Sort by start, then compare neighbours",
        "explain": "Once intervals are sorted by start, each one can only overlap its neighbours. One pass then "
                   "compares each interval with the one before it, or with the last one you kept, instead of "
                   "every pair: O(n log n) for the sort and O(n) for the pass.",
    },
    "intervals.earliest_end": {
        "name": "Earliest end first",
        "explain": "To keep the most intervals that don't overlap, sort by END and keep each one that starts at or "
                   "after the last kept end. The interval that ends first leaves the most room for the rest, so "
                   "taking it is never a mistake.",
    },
```

- [ ] **Step 4: Re-rank `non_overlapping`.** In `non_overlapping.py` (CRLF line endings):
  - Header: replace `[medium]` with `[easy]` (the line was 86 wide and becomes 84).
  - Replace `Aim for:  O(n log n) greedy.` with `Aim for:  O(n log n) greedy. The last test has 20,000 intervals.`
  - Add above `TESTS = `:

```python
def _big():
    import random
    out = [[i, i + 2] for i in range(20_000)]     # chained overlaps: keep every other one
    random.Random(5).shuffle(out)
    return out
```

  - Change the end of the `TESTS` line from `+ _cases()` to `+ _cases() + [((_big(),), 10_000)]`.

- [ ] **Step 5: Tag.**

```bash
python $TAG course/2_core_patterns/10_sorting_and_intervals overlaps=:intervals.overlap insert_interval=intervals.overlap:intervals.merge can_attend_meetings=intervals.overlap:intervals.sort_by_start non_overlapping=intervals.overlap:intervals.earliest_end largest_number= merge_intervals=intervals.overlap,intervals.merge,intervals.sort_by_start summary_ranges=bsearch.first_true,intervals.merge range_module=bsearch.first_true,intervals.overlap,intervals.merge free_slots=intervals.overlap,intervals.merge,intervals.sort_by_start
```

  Expected: 9 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 10_ coverage`. Expected: 9 `ok` lines;
  `ok   technique coverage … 42 techniques, 262 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course tests/test_coverage.py
git commit -m "Stage 2 audit: topic 10 tagged" -m "non_overlapping is now easy and teaches earliest end first, which pick_talks relies on." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 7: Topic 11, greedy

**Files:**
- Modify: `course/techniques.py` (3 entries)
- Create: `course/2_core_patterns/11_greedy/min_suffix_flips.py`, `solutions/min_suffix_flips.py`
- Modify: every other problem file in `11_greedy/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage2Audit`, `TAG` (Task 1); `prefix.difference` (Task 4),
  `intervals.earliest_end` (Task 6), `array.left_right_passes` (Stage 1).
- Produces: `greedy.kadane`, `greedy.farthest_reach`, `greedy.forced_first`; the title "Minimum
  Suffix Flips" and the name "The forced first move", which Task 8 reads.

- [ ] **Step 1: Write the failing tests.** Add to `Stage2Audit`:

```python
    def test_topic_11(self):
        self.assert_audited("11_greedy")
        self.assert_teaches({"extend_or_restart": ["greedy.kadane"], "min_jumps": ["greedy.farthest_reach"],
                             "min_suffix_flips": ["greedy.forced_first"]})
        self.assert_uses({"min_k_bit_flips": ["prefix.difference", "greedy.forced_first"],
                          "hand_of_straights": ["greedy.forced_first"], "gas_station": ["greedy.kadane"],
                          "min_taps": ["greedy.farthest_reach"], "candy": ["array.left_right_passes"],
                          "pick_talks": ["intervals.earliest_end"], "patching_array": []})
        self.assertEqual(self.problems["min_suffix_flips"]["difficulty"], "easy")

    def test_teacher_big_tests_reject_the_naive_solution(self):
        # Solving a teacher marks its technique learned, so its big test must time out without it.
        def big(name, ok):
            self.assertTrue(any(ok(args, want) for args, want in self.cases_of(name)), name)
        big("merge_sorted", lambda ab, w: len(ab[1]) >= 100_000 and len(ab[0]) >= 100_000)      # insort: O(n * m)
        big("nice_subarrays", lambda a, w: len(a[0]) >= 100_000 and w >= 50_000_000)          # one step per answer
        big("zero_sum_subarrays", lambda a, w: len(a[0]) >= 100_000)                           # every subarray
        big("range_additions", lambda a, w: sum(r - l + 1 for l, r, _ in a[1]) >= 1_000_000_000)
        big("min_suffix_flips", lambda a, w: len(a[0]) >= 100_000 and w >= 50_000)            # flip per press
        big("min_subarray_len", lambda a, w: len(a[1]) >= 100_000 and w >= 10_000)            # every start
        big("non_overlapping", lambda a, w: len(a[0]) >= 20_000)                               # O(n²) DP
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_11` fails on unaudited problems, and the big-test check fails on `min_suffix_flips`
  (no such file yet).

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "greedy.kadane": {
        "name": "Extend or restart",
        "explain": "Walking left to right, the best run ending at x either continues the run before it or starts "
                   "fresh at x: `cur = max(x, cur + x)`. A run with a negative total only drags down whatever "
                   "follows, so drop it and restart. This is Kadane's algorithm: O(n) time, O(1) space.",
    },
    "greedy.farthest_reach": {
        "name": "Farthest reach",
        "explain": "Walk left to right keeping `far`, the farthest index you can reach so far: "
                   "`far = max(far, i + nums[i])`. If i ever passes far, you're stuck. To count jumps, treat each "
                   "jump as a level: when i reaches the end of the current level, jump once, and the next level "
                   "ends at far.",
    },
    "greedy.forced_first": {
        "name": "The forced first move",
        "explain": "Go left to right. Often the first thing that's still wrong can only be fixed one way: a flip "
                   "must start there, or the smallest card must start a group. Make that forced move and carry "
                   "on. There's no choice to search, so it's one pass.",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/2_core_patterns/11_greedy/min_suffix_flips.py`:

```python
"""
Minimum Suffix Flips                                                          [easy]

A row of bulbs starts all off. Pressing switch i flips every bulb from i to the
end of the row: on becomes off and off becomes on. `target` says which bulbs
should end up on ("1") and off ("0"). Return the fewest presses.

Example:
    min_suffix_flips("10111")  ->  3      press 0: 11111, press 1: 10000, press 2: 10111
    min_suffix_flips("000")    ->  0

Aim for:  O(n). The last test has 100,000 bulbs: really flipping the rest of the
          row on every press is O(n²) and times out.
Hint:     Go left to right. The first wrong bulb can only be fixed by its own
          switch: the bulbs to its left are already right, and switches further
          right can't reach it. So that press is forced. Don't flip anything: count
          the presses so far. A bulb is on exactly when that count is odd.
"""


def min_suffix_flips(target: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["greedy.forced_first"]
USES = []

TESTS = [
    (("10111",), 3),
    (("000",), 0),
    (("101",), 3),
    (("1",), 1),
    (("0",), 0),
    (("00111",), 1),
    (("110011",), 3),
    (("10" * 50_000,), 100_000),
]
```

  Create `solutions/min_suffix_flips.py`:

```python
def min_suffix_flips(target: str) -> int:
    # The first wrong bulb forces a press there. A bulb is on when the presses so far are odd. O(n).
    presses = 0
    for want in target:
        on = presses % 2 == 1
        if on != (want == "1"):
            presses += 1
    return presses
```

- [ ] **Step 5: Tag.**

```bash
python $TAG course/2_core_patterns/11_greedy extend_or_restart=:greedy.kadane min_jumps=:greedy.farthest_reach gas_station=greedy.kadane hand_of_straights=greedy.forced_first can_jump=greedy.farthest_reach max_subarray=greedy.kadane merge_triplets= partition_labels=greedy.farthest_reach valid_paren_string= candy=array.left_right_passes min_k_bit_flips=prefix.difference,greedy.forced_first min_taps=greedy.farthest_reach patching_array= pick_talks=intervals.earliest_end
```

  Expected: 14 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 11_ coverage`. Expected: 15 `ok` lines;
  `ok   technique coverage … 45 techniques, 248 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 2 audit: topic 11 tagged, with min_suffix_flips" -m "The forced first move gets a basic problem before hand_of_straights and min_k_bit_flips rely on it. Teacher big tests are checked against the naive solution." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 8: README, browser check and full verification

**Files:**
- Modify: `README.md` (exercise count)
- Create: `tests/browser/stage_2.mjs`
- Modify: `tests/browser/README.md`

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: README.** Replace `34 topics in 6 stages, 394 coding exercises` with
  `34 topics in 6 stages, 399 coding exercises` (394 plus the five new problems).

- [ ] **Step 2: Write the browser scenario.** Create `tests/browser/stage_2.mjs`. Its helpers
  (`solve`, `post`, `text`, `techList`) and its opening (`open`, then `/api/placement` with
  `{ door: "skip" }`) are copied from `stage_1.mjs`. Its checks, in this order:

  1. `#/t/07_sliding_window`: `techList` joined with `" | "` equals
     `Fixed-size window | Growing and shrinking a window | Shortest window | Counting with a window`.
  2. `#/t/10_sorting_and_intervals`: equals
     `Do two intervals overlap? | Absorbing an overlap | Sort by start, then compare neighbours | Earliest end first`.
  3. Solve `slide_sum`, then `longest_k_distinct` (two checks).
  4. `#/p/min_subarray_len`: `.tech-new h4` is `New technique: Shortest window`.
  5. `#/p/subarrays_k_distinct`: `.reveal-box` includes `This uses Counting with a window` and
     `Subarrays With k Odd Numbers teaches it`.
  6. Solve `nice_subarrays`; then `#/t/07_sliding_window`'s list includes `✓Counting with a window`.
  7. `/api/reset-progress`, placement `skip` again; solve `lower_bound` and `ship_capacity`; then
     `#/p/smallest_distance_pair`: `.tech-banner` includes `This uses Counting with a window` and
     `Subarrays With k Odd Numbers`.
  8. Solve `extend_or_restart` and `min_jumps`; then `#/p/min_k_bit_flips`: `.reveal-box`
     includes `This uses The forced first move` and `Minimum Suffix Flips teaches it`. (It also
     uses 08's difference array, which is unsolved: that one is a banner, not the lock.)
  9. No console errors.

  That is 15 `check` calls.

- [ ] **Step 3: Mention it.** In `tests/browser/README.md`, after the line
  `    bash tests/browser/fresh.sh 8171 stage_1.mjs`, add `    bash tests/browser/fresh.sh 8172 stage_2.mjs`.

- [ ] **Step 4: Run** `node --check tests/browser/stage_2.mjs && bash tests/browser/fresh.sh 8172 stage_2.mjs`.
  Expected: 15 of 15 pass. If a technique list fails only on order, compare with `items` for that
  topic from `server.load_course()`; fix the expectation only if the ladder order is right.

- [ ] **Step 5: Earlier scenarios still pass.** Run `bash tests/browser/fresh.sh 8170 technique_coverage.mjs`
  (23 of 23) and `bash tests/browser/fresh.sh 8171 stage_1.mjs` (14 of 14), then delete
  `tests/browser/technique_coverage.png` if the first one leaves it.

- [ ] **Step 6: Phase 1 still works.** Run `bash fresh.sh <port> tN.mjs` for t4 … t8 from this
  session's `scratchpad/cdp` folder. Expected: 54 checks pass in total. Stage 2 doesn't touch
  topic 01, so no expectation should change.

- [ ] **Step 7: Unit tests.** Run `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: The whole course.** Run `python server.py --check`. Expected: every problem `ok`
  (399), `ok   starting check`, `ok   technique coverage … 45 techniques, 248 problem(s) not
  audited yet`, `All good.` This takes a few minutes.

- [ ] **Step 9: Commit**

```bash
git add README.md tests/browser/stage_2.mjs tests/browser/README.md
git commit -m "Stage 2 audit: README count and a browser check for topic 07's techniques" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
