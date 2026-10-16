# Technique coverage, Part 2 Stage 1: audit topics 01–05 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in topics 01–05 lists the techniques it uses. Each of those techniques is
taught by a basic problem that comes earlier, and no Stage 1 problem relies on a later topic.

**Architecture:** Content work plus one small server fix. 16 techniques join `course/techniques.py`.
Every Stage 1 problem file gets `USES` (and `TEACHES` on teachers). Five new problems are added:
four easy teachers and one hard. Four problems move to the topic of their last prerequisite, and
one is re-ranked to easy. `ladder_order` stops letting a lower-rank teacher push a problem down
inside its own rank. A `Stage1Audit` test class pins all of it.

**Tech Stack:** Python 3.12 stdlib, `unittest`, the existing `--check` self-check, and the Node
headless-Chrome scenarios in `tests/browser/`.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md` (Part 2: the content
audit, and "Fixing a gap").

## Global Constraints

- No new dependencies: no pip or npm packages.
- Problem names, topic ids and drill keys never change. Moving a file between topic folders is
  allowed; progress, saved code and study plans are keyed by name.
- `USES` and `TEACHES` go **after** the problem's function or class, directly above `TESTS =` or
  `STEPS =`. Assignments above the first `def` are copied into the starter code.
- A teacher is a `snippet`, `guided` or `easy` problem. Every technique has exactly one teacher,
  and it comes before every problem that uses the technique.
- A technique from a later topic is never allowed. Cross-topic gaps are fixed in the earlier topic.
- Every topic keeps at least two hard problems (README: "at least two hard problems in every topic").
- Problem headers are 84 characters wide: the title, spaces, then `[easy]` (or another kind) at the end.
- Course files use CRLF line endings in the working tree (`core.autocrlf=true`). Edits keep them.
- Tests: `python -m unittest discover -s tests` (one file: add `-p "test_x.py"`). Self-check:
  `python server.py --check <filters>`. A filter matches a problem name or a topic id; `coverage`
  runs the technique check.
- End every commit message with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## What counts as a technique

The spec defines a technique as "a reusable idea a learner can know or not know", and excludes
plain Python features. The audit applies that as follows, and Task 1 writes it into the spec so
later stages use the same rule:

- **A technique** is a method with a recognisable shape that changes how you solve the problem:
  what you store, how you walk, or what you look up. Examples: a seen set, best so far, left and
  right passes, carrying digits, memoisation.
- **Not a technique:** using a Python tool for what it plainly does: `Counter` to count, `sorted`
  with a key, a tuple as a dict key, slicing, `zip`, `divmod`, string methods. The toolkit topic
  covers those.
- A topic's snippet and guided problem register the topic's core idea when later problems rely on
  it, like `grid.neighbors` in Part 1.
- A medium or hard problem may keep **one insight of its own**: the step its hint gives away.
  Examples: count the opposite (`count_bad_pairs`), or sort so the absolute value disappears
  (`sum_pair_distances`). That insight becomes a technique with its own basic problem only when it
  recurs in other problems.

## Audit results

Read for every Stage 1 problem: statement, hint and reference solution.

**New techniques (16), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `hash.set_lookup` | Set for fast lookups | `common_count` (guided, 01) | reuse |
| `scan.best_so_far` | Best so far | `max_profit` (easy) | **move** from 07 Sliding window, where its hint was best-so-far, not a window |
| `pairs.split_by_index` | Separating i from j | `best_sightseeing_pair` | **re-rank** hard → easy; it is built around exactly this |
| `hash.count_pairs` | Counting pairs with a dict | `equal_pairs` | **new** easy in 01 |
| `array.wrap_index` | Wrapping around with % | `rotate_index` (snippet, 03) | reuse |
| `matrix.boundaries` | Shrinking boundaries | `spiral_order` (guided, 03) | reuse |
| `array.write_pointer` | Write pointer | `move_zeroes` (easy, 03) | reuse |
| `math.carry` | Carrying digits | `plus_one` (easy, 03) | reuse |
| `array.left_right_passes` | Left and right passes | `distance_to_char` | **new** easy in 03 |
| `hash.seen_set` | Seen set | `first_repeat` (snippet, 04) | reuse |
| `hash.run_starts` | Starting runs at their first number | `longest_consecutive` (guided, 04) | reuse |
| `hash.complement` | Complement lookup | `two_sum` (easy, 04) | reuse |
| `hash.group_key` | Grouping by a computed key | `group_by_ends` | **new** easy in 04 |
| `recursion.trust` | Base case and a smaller call | `digit_sum` (snippet, 05) | reuse |
| `recursion.memo` | Memoisation | `count_paths` (guided, 05) | reuse: it already uses `@lru_cache`, so `scramble_string` needs no move |
| `recursion.parse` | Parsing with recursion | `min_max_expr` | **new** easy in 05 |

**Problems that rely on a later topic, moved to the topic of their last prerequisite** (Stage 2
tags them there):

| Problem | From | To | Needs |
|---|---|---|---|
| `concat_all_words` | 04 | `07_sliding_window` | a sliding window over word-sized pieces |
| `submatrix_sum_target` | 04 | `08_prefix_sums` | prefix sums plus a dict of earlier sums |
| `min_k_bit_flips` | 03 | `11_greedy` | the forced greedy choice, plus counting where flips end |

**One new hard:** topic 04 loses two hards to the moves, so `grid_illumination` (hard) joins it. It
uses only hashing: counts per row, column and diagonal (`r - c`, `r + c`), and a set of lamps.

**Tags for every problem.** "own" names the insight a medium or hard keeps for itself.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 01 | `halvings` (snippet) | | | |
| 01 | `common_count` (guided) | `hash.set_lookup` | | |
| 01 | `common_elements` | | `hash.set_lookup` | |
| 01 | `missing_number` | | | the sum formula is in the hint |
| 01 | `max_profit` (moved in) | `scan.best_so_far` | | |
| 01 | `equal_pairs` (new) | `hash.count_pairs` | | |
| 01 | `best_sightseeing_pair` (now easy) | `pairs.split_by_index` | `scan.best_so_far` | |
| 01 | `count_bad_pairs` (hard) | | `hash.count_pairs`, `pairs.split_by_index` | own: count the opposite |
| 01 | `sum_pair_distances` (hard) | | | own: sort, then x pairs with the k smaller ones at once |
| 01 | `top_visitors` (build) | | | `Counter` plus a sort key |
| 02 | `last_seen`, `word_frequencies`, `reverse_words`, `running_sum`, `expense_report` | | | toolkit: dicts, `Counter`, sort keys, `split`, `accumulate` |
| 02 | `second_largest` | | `scan.best_so_far` | the best two so far |
| 02 | `number_to_words`, `rank_teams`, `text_justify` (hard) | | | own: groups of three digits; a list as a sort key; packing lines |
| 03 | `rotate_index` (snippet) | `array.wrap_index` | | |
| 03 | `spiral_order` (guided) | `matrix.boundaries` | | |
| 03 | `longest_common_prefix` | | | `zip(*words)` |
| 03 | `move_zeroes` | `array.write_pointer` | | |
| 03 | `plus_one` | `math.carry` | | |
| 03 | `distance_to_char` (new) | `array.left_right_passes` | | |
| 03 | `detect_squares` | | `hash.set_lookup` | own: fix the diagonal corner |
| 03 | `multiply_strings` | | `math.carry` | own: digit i times digit j lands at i + j + 1 |
| 03 | `product_except_self` | | `array.left_right_passes` | |
| 03 | `rotate_array` | | `array.wrap_index` | slicing does the rest |
| 03 | `rotate_image` | | | own: transpose, then mirror |
| 03 | `set_matrix_zeroes` | | `hash.set_lookup` | own: record first, clear in a second pass |
| 03 | `first_missing_positive` (hard) | | | own: the list as its own lookup table |
| 03 | `max_chunks_to_sorted` (hard) | | `array.left_right_passes`, `scan.best_so_far` | own: cut where left max ≤ right min |
| 03 | `format_table` (build) | | | |
| 04 | `first_repeat` (snippet) | `hash.seen_set` | | |
| 04 | `longest_consecutive` (guided) | `hash.run_starts` | `hash.set_lookup` | |
| 04 | `contains_duplicate`, `is_happy` | | `hash.seen_set` | `is_happy`'s reference switches to the seen set (Task 4) |
| 04 | `two_sum` | `hash.complement` | | |
| 04 | `valid_anagram` | | | `Counter` |
| 04 | `group_by_ends` (new) | `hash.group_key` | | |
| 04 | `encode_decode` | | | own: length-prefix each string |
| 04 | `group_anagrams` | | `hash.group_key` | own: sorted letters as the key |
| 04 | `top_k_frequent` | | | own: buckets by count (or `most_common`) |
| 04 | `is_valid_sudoku` | | `hash.seen_set` | own: the box index |
| 04 | `max_equal_freq` (hard) | | | own: counts of counts |
| 04 | `grid_illumination` (new hard) | | `hash.group_key`, `hash.set_lookup` | own: switch lamps off by updating counts |
| 04 | `word_index` (build) | | `hash.set_lookup` | |
| 05 | `digit_sum` (snippet) | `recursion.trust` | | |
| 05 | `count_paths` (guided) | `recursion.memo` | `recursion.trust` | |
| 05 | `flatten_list` | | `recursion.trust` | |
| 05 | `min_max_expr` (new) | `recursion.parse` | `recursion.trust` | |
| 05 | `power` | | `recursion.trust` | own: halve, and square once |
| 05 | `calculate`, `count_of_atoms` (hard) | | `recursion.parse`, `recursion.trust` | |
| 05 | `scramble_string` (hard) | | `recursion.memo`, `recursion.trust` | |
| 05 | `render_folders` (build) | | `recursion.trust` | |

`USES` lists techniques in teaching order. The in-topic lock names the first unsolved teacher in
`USES`, so `count_bad_pairs` points at `equal_pairs` before `best_sightseeing_pair`, which matches
the ladder.

**Order fix.** `ladder_order` currently counts every same-topic teacher when it works out a
problem's teaching depth, including snippets and guided problems. Those already come first because
of their rank. Counting them pushes easy problems that use a snippet's technique below unrelated
easies: Contains Duplicate would drop below Valid Anagram. This is the deferred Part 1 minor
"ladder depth reorders unrelated same-rank problems". Only teachers of the **same rank** should
count. The spec already says "within a rank".

## Review Focus

1. **Moved problems keep their history.** A learner who solved `max_profit` in Sliding window sees
   it solved in topic 01, and every study-plan item still exists. Owners: the Task 1 test
   `test_every_plan_item_exists` (already in `GraphTraversalPilot`), and the Task 6 browser check
   "solving max_profit ticks Best so far on topic 01".
2. **Tags never leak into a starter.** A learner's editor must not show `USES = [...]`. Owner: the
   Task 1 test `test_tags_stay_out_of_starters`, run across the whole course.
3. **Re-ranking and moving keep two hards in every Stage 1 topic.** Owner: the Task 4 test
   `test_every_stage_1_topic_keeps_two_hard_problems`.
4. **The order fix keeps real teaching chains intact.** A same-rank teacher still comes first.
   Owners: the existing `LadderOrder` tests, and the Task 1 test
   `test_lower_rank_teachers_do_not_reorder_a_rank`.
5. **New problems behave like the rest.** Starters report `todo`, reference solutions pass, and big
   tests reject the brute force. Owners: `--check` in Tasks 2–5. Expected values come from these
   exact solutions, cross-checked against brute force while this plan was written.

---

### Task 1: The rule, the order fix and the moves

**Files:**
- Modify: `server.py` (`ladder_order`, around line 494)
- Modify: `tests/test_techniques.py` (`LadderOrder`)
- Modify: `tests/test_coverage.py` (new `Stage1Audit` class)
- Move: `course/2_core_patterns/07_sliding_window/max_profit.py` → `course/1_foundations/01_big_o_in_practice/`
- Move: `course/1_foundations/03_arrays_and_strings/min_k_bit_flips.py` → `course/2_core_patterns/11_greedy/`
- Move: `course/1_foundations/04_hashing/submatrix_sum_target.py` → `course/2_core_patterns/08_prefix_sums/`
- Move: `course/1_foundations/04_hashing/concat_all_words.py` → `course/2_core_patterns/07_sliding_window/`
- Modify: `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`
- Create: `.superpowers/sdd/2026-10-16-technique-coverage-stage-1/tag.py` (git-ignored helper)

**Interfaces:**
- Produces: `Stage1Audit` with helpers `items(topic_id)`, `assert_audited(topic_id)`,
  `assert_uses({name: [ids]})` (compares as sets) and `assert_teaches({name: [ids]})` (compares
  lists). Tasks 2–5 add one test method each.
- Produces: `tag.py FOLDER NAME=USES[:TEACHES] ...`, where USES and TEACHES are comma-separated and
  either may be empty. It inserts the tags above `TESTS =` or `STEPS =`, keeps the file's line
  endings, and refuses files that are already tagged.

- [ ] **Step 1: Write the failing tests.** In `tests/test_techniques.py`, add to `LadderOrder`
  after `test_chains_sort_in_teaching_order`:

```python
    def test_lower_rank_teachers_do_not_reorder_a_rank(self):
        found = [prob("b_user", 2, title="B", uses=["t.x"]), prob("a_plain", 2, title="Z"), prob("snip", 0, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["snip", "b_user", "a_plain"])
```

  In `tests/test_coverage.py`, add above `if __name__ == "__main__":`:

```python
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

    def test_tags_stay_out_of_starters(self):
        leaks = [n for n, p in self.problems.items() if "USES" in p["starter"] or "TEACHES" in p["starter"]]
        self.assertEqual(leaks, [])
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests`. Expected: two failures. `test_lower_rank_teachers_do_not_reorder_a_rank` gets `['snip', 'a_plain', 'b_user']`.
  `test_problems_moved_to_the_topic_of_their_last_prerequisite` reports `max_profit` in
  `07_sliding_window`. `test_tags_stay_out_of_starters` passes already: it guards Tasks 2–5.

- [ ] **Step 3: Fix `ladder_order`.** In `server.py`, replace the `deps = ...` line inside `d()`:

```python
        deps = [teacher[t] for t in _tag_list(by_name[name].get("uses")) if teacher.get(t) not in (None, name)]
```

  with:

```python
        deps = [teacher[t] for t in _tag_list(by_name[name].get("uses"))
                if teacher.get(t) not in (None, name) and by_name[teacher[t]]["rank"] == by_name[name]["rank"]]
```

  and in the docstring of `ladder_order`, change `every same-topic problem that` to
  `every same-topic, same-rank problem that`.

- [ ] **Step 4: Move the four problems.**

```bash
git mv course/2_core_patterns/07_sliding_window/max_profit.py course/1_foundations/01_big_o_in_practice/max_profit.py
git mv course/1_foundations/03_arrays_and_strings/min_k_bit_flips.py course/2_core_patterns/11_greedy/min_k_bit_flips.py
git mv course/1_foundations/04_hashing/submatrix_sum_target.py course/2_core_patterns/08_prefix_sums/submatrix_sum_target.py
git mv course/1_foundations/04_hashing/concat_all_words.py course/2_core_patterns/07_sliding_window/concat_all_words.py
```

  In `max_profit.py`, replace the header line
  `Best Time to Buy and Sell Stock                              [easy] · sliding window`
  with the 84-character
  `Best Time to Buy and Sell Stock                                               [easy]`.
  Nothing else changes; its solution in `solutions/` is keyed by name.

- [ ] **Step 5: Write the rule into the spec.** In
  `docs/superpowers/specs/2026-10-16-technique-coverage-design.md`, insert this section between the
  end of `## Assumptions` and `## Why`:

```markdown
## What counts as a technique

Settled in the Stage 1 audit, for every later stage:

- **A technique** is a method with a recognisable shape that changes how you solve the problem:
  what you store, how you walk, or what you look up. Examples: a seen set, best so far, left and
  right passes, carrying digits, memoisation.
- **Not a technique:** using a Python tool for what it plainly does: `Counter` to count, `sorted`
  with a key, a tuple as a dict key, slicing, `zip`, `divmod`, string methods. The toolkit topic
  covers those.
- A topic's snippet and guided problem register the topic's core idea when later problems rely on
  it, like grid neighbours.
- A medium or hard problem may keep **one insight of its own**: the step its hint gives away, such
  as "count the opposite". It becomes a technique, with its own basic problem, only when it recurs
  in other problems.
```

  In the same file, change the table row
  ``| `scramble_string` (05) | memoisation | 23 DP |``
  to
  ``| `scramble_string` (05) | memoisation | 23 DP (fixed: `count_paths`, 05's guided problem, already teaches it) |``.

- [ ] **Step 6: The tagging helper.** Run
  `bash ~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/subagent-driven-development/scripts/sdd-workspace docs/superpowers/plans/2026-10-16-technique-coverage-stage-1.md`
  to create the workspace (it prints the folder). Then create `tag.py` in that folder:

```python
"""Tag problem files: python tag.py FOLDER NAME=USES[:TEACHES] ...

USES and TEACHES are comma-separated technique ids; either may be empty (`halvings=` tags USES = []).
The tags go directly above the file's `TESTS =` or `STEPS =` line, with the file's own line endings."""
import json
import re
import sys
from pathlib import Path


def tag(path, uses, teaches):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    if re.search(r"^(USES|TEACHES) ?=", text, re.M):
        sys.exit(f"{path}: already tagged")
    m = re.search(r"^(TESTS|STEPS) ?=", text, re.M)
    if not m:
        sys.exit(f"{path}: no TESTS or STEPS line")
    eol = "\r\n" if "\r\n" in text else "\n"
    block = (f"TEACHES = {json.dumps(teaches)}{eol}" if teaches else "") + f"USES = {json.dumps(uses)}{eol}{eol}"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text[:m.start()] + block + text[m.start():])


if __name__ == "__main__":
    folder = Path(sys.argv[1])
    for arg in sys.argv[2:]:
        name, _, spec = arg.partition("=")
        uses, _, teaches = spec.partition(":")
        tag(folder / f"{name}.py", [u for u in uses.split(",") if u], [t for t in teaches.split(",") if t])
        print("tagged", name)
```

  Later tasks run it as `python <workspace>/tag.py ...`, with the folder this step printed.

- [ ] **Step 7: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: Run**
  `python server.py --check max_profit min_k_bit_flips submatrix_sum_target concat_all_words coverage`.
  Expected: four `ok` lines, under topics 01, 11, 08 and 07; then
  `ok   technique coverage … 11 techniques, 369 problem(s) not audited yet`; then `All good.`

- [ ] **Step 9: Commit**

```bash
git add server.py tests/test_techniques.py tests/test_coverage.py course docs/superpowers/specs/2026-10-16-technique-coverage-design.md
git commit -m "Stage 1 audit setup: what counts as a technique, same-rank teaching order, four problems moved" -m "max_profit moves to Big-O in practice to teach best-so-far. min_k_bit_flips, submatrix_sum_target and concat_all_words move to the topics that teach what they need." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Topics 01 and 02

**Files:**
- Modify: `course/techniques.py` (4 entries)
- Create: `course/1_foundations/01_big_o_in_practice/equal_pairs.py`, `solutions/equal_pairs.py`
- Modify: `course/1_foundations/01_big_o_in_practice/best_sightseeing_pair.py` (re-rank), every
  other file in `01_big_o_in_practice/` and `02_python_toolkit/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage1Audit` and `tag.py` (Task 1).
- Produces: `hash.set_lookup` and `scan.best_so_far`, which Tasks 3 and 4 use; `equal_pairs`
  (title "Matching Pairs") and the technique names that Task 6's browser check reads.

- [ ] **Step 1: Write the failing test.** Add to `Stage1Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topics_01_and_02` fails: topic 01 lists unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above the line
  `    "grid.neighbors": {`:

```python
    "hash.set_lookup": {
        "name": "Set for fast lookups",
        "explain": "`x in some_list` scans the whole list, but `x in some_set` is one hash lookup. When a loop keeps "
                   "asking \"is x in there?\", build a set (or dict) once before the loop and the inner search "
                   "disappears: O(n * m) becomes O(n + m).",
    },
    "scan.best_so_far": {
        "name": "Best so far",
        "explain": "To find the best pair i < j, walk j once and remember the best i you've passed: the smallest "
                   "price, the largest value. Each j only needs that one number, so every pair is checked in O(n) "
                   "instead of O(n²).",
    },
    "pairs.split_by_index": {
        "name": "Separating i from j",
        "explain": "Rewrite a pair's score or condition so one part uses only i and the other only j: "
                   "`values[i] + values[j] + i - j` is `(values[i] + i) + (values[j] - j)`. Then each index has "
                   "its own number, and best so far or a dict of counts does the rest.",
    },
    "hash.count_pairs": {
        "name": "Counting pairs with a dict",
        "explain": "To count pairs i < j with equal values, walk once with a dict of how many times each value has "
                   "appeared so far. A new x pairs with every earlier x, so add `seen[x]` to the answer, then "
                   "increase `seen[x]`. One pass instead of checking every pair.",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/1_foundations/01_big_o_in_practice/equal_pairs.py`:

```python
"""
Matching Pairs                                                                [easy]

Count the pairs of indexes i < j where nums[i] == nums[j].

`nums` can hold 100,000 numbers, so checking every pair is far too slow.

Example:
    equal_pairs([1, 2, 3, 1, 1, 3])  ->  4      (0, 3), (0, 4), (3, 4) and (2, 5)

Aim for:  O(n), one pass.
Hint:     Walk the list once with a dict of how many times you've seen each value so far.
          A new x makes a pair with every earlier x: add seen[x] to the answer, then add 1
          to seen[x].
"""


def equal_pairs(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["hash.count_pairs"]
USES = []

TESTS = [
    (([1, 2, 3, 1, 1, 3],), 4),
    (([1, 1, 1, 1],), 6),
    (([1, 2, 3],), 0),
    (([],), 0),
    (([5],), 0),
    (([2, 2],), 1),
    (([-1, 3, -1, 3, -1],), 4),
    (([k % 1000 for k in range(100_000)],), 4_950_000),
]
```

  Create `solutions/equal_pairs.py`:

```python
def equal_pairs(nums: list[int]) -> int:
    # Each x pairs with every earlier x: add how many came before, then count this one. O(n).
    seen, pairs = {}, 0
    for x in nums:
        pairs += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return pairs
```

- [ ] **Step 5: Re-rank.** In `best_sightseeing_pair.py`, change `[hard]` to `[easy]` on the header
  line (same width). Nothing else changes.

- [ ] **Step 6: Tag.** Run (with the workspace folder from Task 1 in place of `<workspace>`):

```bash
python <workspace>/tag.py course/1_foundations/01_big_o_in_practice halvings= common_count=:hash.set_lookup common_elements=hash.set_lookup missing_number= max_profit=:scan.best_so_far best_sightseeing_pair=scan.best_so_far:pairs.split_by_index count_bad_pairs=hash.count_pairs,pairs.split_by_index sum_pair_distances= top_visitors=
python <workspace>/tag.py course/1_foundations/02_python_toolkit last_seen= word_frequencies= reverse_words= running_sum= second_largest=scan.best_so_far number_to_words= rank_teams= text_justify= expense_report=
```

  Expected: 18 `tagged` lines. Spot-check one: `git diff course/1_foundations/01_big_o_in_practice/count_bad_pairs.py`
  shows two added lines (`USES = ["hash.count_pairs", "pairs.split_by_index"]` and a blank line)
  directly above `TESTS = [`, and no other changes.

- [ ] **Step 7: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: Run** `python server.py --check 01_ 02_ coverage`. Expected: 19 `ok` lines (10 in
  01, 9 in 02); `ok   technique coverage … 15 techniques, 351 problem(s) not audited yet`;
  `All good.`

- [ ] **Step 9: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 1 audit: topics 01 and 02 tagged" -m "Best so far, separating i from j and counting pairs get basic problems: max_profit, best_sightseeing_pair (now easy) and the new equal_pairs." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: Topic 03

**Files:**
- Modify: `course/techniques.py` (5 entries)
- Create: `course/1_foundations/03_arrays_and_strings/distance_to_char.py`, `solutions/distance_to_char.py`
- Modify: every other file in `03_arrays_and_strings/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `hash.set_lookup`, `scan.best_so_far` (Task 2); `Stage1Audit`, `tag.py` (Task 1).
- Produces: `array.wrap_index`, `matrix.boundaries`, `array.write_pointer`, `math.carry`,
  `array.left_right_passes`.

- [ ] **Step 1: Write the failing test.** Add to `Stage1Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_03` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`
  (so after Task 2's entries):

```python
    "array.wrap_index": {
        "name": "Wrapping around with %",
        "explain": "`(i + k) % n` keeps an index inside 0..n - 1 however far it moves, and in Python it works for "
                   "negative k too. Use it for anything circular: rotating a list, a clock, a ring of seats. Doing "
                   "`k %= n` first also stops a huge k from going round extra times.",
    },
    "matrix.boundaries": {
        "name": "Shrinking boundaries",
        "explain": "Keep four edges: top, bottom, left and right. Walk along one edge, then move it inward by one, "
                   "and stop once top > bottom or left > right. Check those again before the third and fourth "
                   "sides, or a single row or column gets read twice.",
    },
    "array.write_pointer": {
        "name": "Write pointer",
        "explain": "Keep an index `w` for where the next kept item goes. Walk the list, copy each item you keep to "
                   "`a[w]` and add 1 to `w`. Everything before `w` is the answer so far, built in place in one pass "
                   "with no extra list.",
    },
    "math.carry": {
        "name": "Carrying digits",
        "explain": "Add digit by digit from the right, as on paper. A column's total gives the digit `total % 10` "
                   "and carries `total // 10` into the next column to the left. A carry left over at the end "
                   "becomes a new leading digit.",
    },
    "array.left_right_passes": {
        "name": "Left and right passes",
        "explain": "When the answer at i depends on both sides of i, make one pass left to right that carries what "
                   "you know about everything before i, and one pass right to left for everything after it. "
                   "Combine the two at each i: two O(n) passes instead of searching both ways from every index.",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/1_foundations/03_arrays_and_strings/distance_to_char.py`:

```python
"""
Shortest Distance to a Letter                                                 [easy]

For every index i of `s`, find how far it is to the nearest copy of the letter
`c`, and return those distances as a list. `c` appears in `s` at least once.

Example:
    distance_to_char("loveleetcode", "e")  ->  [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]

Aim for:  O(n): one pass from the left and one from the right. Searching outwards
          from every index is O(n²) on the big test.
Hint:     Left to right, remember where you last saw c and write i - last (use a big
          number before the first c). Then right to left, remember the last c from
          that side and keep the smaller of the two distances.
"""


def distance_to_char(s: str, c: str) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["array.left_right_passes"]
USES = []

TESTS = [
    (("loveleetcode", "e"), [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]),
    (("aaab", "b"), [3, 2, 1, 0]),
    (("a", "a"), [0]),
    (("baab", "b"), [0, 1, 1, 0]),
    (("abcde", "c"), [2, 1, 0, 1, 2]),
    (("cxxxxc", "c"), [0, 1, 2, 2, 1, 0]),
    (("c" + "x" * 99_998 + "c", "c"), [min(i, 99_999 - i) for i in range(100_000)]),
]
```

  Create `solutions/distance_to_char.py`:

```python
def distance_to_char(s: str, c: str) -> list[int]:
    # Left pass: distance to the last c on the left. Right pass: keep the smaller of that and
    # the distance to the next c on the right. O(n).
    n = len(s)
    answer = [n] * n
    last = None
    for i in range(n):
        if s[i] == c:
            last = i
        if last is not None:
            answer[i] = i - last
    last = None
    for i in range(n - 1, -1, -1):
        if s[i] == c:
            last = i
        if last is not None:
            answer[i] = min(answer[i], last - i)
    return answer
```

- [ ] **Step 5: Tag.**

```bash
python <workspace>/tag.py course/1_foundations/03_arrays_and_strings rotate_index=:array.wrap_index spiral_order=:matrix.boundaries longest_common_prefix= move_zeroes=:array.write_pointer plus_one=:math.carry detect_squares=hash.set_lookup multiply_strings=math.carry product_except_self=array.left_right_passes rotate_array=array.wrap_index rotate_image= set_matrix_zeroes=hash.set_lookup first_missing_positive= max_chunks_to_sorted=array.left_right_passes,scan.best_so_far format_table=
```

  Expected: 14 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 03_ coverage`. Expected: 15 `ok` lines;
  `ok   technique coverage … 20 techniques, 337 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 1 audit: topic 03 tagged" -m "Left and right passes get a basic problem, distance_to_char, before product_except_self and max_chunks_to_sorted rely on them." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: Topic 04

**Files:**
- Modify: `course/techniques.py` (4 entries)
- Create: `course/1_foundations/04_hashing/group_by_ends.py`, `solutions/group_by_ends.py`
- Create: `course/1_foundations/04_hashing/grid_illumination.py`, `solutions/grid_illumination.py`
- Modify: `solutions/is_happy.py` (reference uses the seen set)
- Modify: every other file in `04_hashing/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `hash.set_lookup` (Task 2); `Stage1Audit`, `tag.py` (Task 1).
- Produces: `hash.seen_set`, `hash.run_starts`, `hash.complement`, `hash.group_key`.

- [ ] **Step 1: Write the failing tests.** Add to `Stage1Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected: both
  fail. `test_every_stage_1_topic_keeps_two_hard_problems` reports
  `('04_hashing', ['max_equal_freq'])`.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "hash.seen_set": {
        "name": "Seen set",
        "explain": "Walk once with an empty set. For each item, first ask `if x in seen`, and only then "
                   "`seen.add(x)`. The set answers \"have I met this before?\" in O(1), so a repeat or a loop "
                   "shows up the moment it happens.",
    },
    "hash.run_starts": {
        "name": "Starting runs at their first number",
        "explain": "To measure runs of consecutive numbers, put them in a set and only start counting at an x whose "
                   "x - 1 is missing: that x begins a run. Walk up x + 1, x + 2, ... while they're in the set. Each "
                   "number is looked at about twice, so it's O(n) without sorting.",
    },
    "hash.complement": {
        "name": "Complement lookup",
        "explain": "When two values must add up to a target, x's partner is `target - x`. Keep a dict of the values "
                   "you've passed (value → index) and look the partner up before you add x, so x can't pair with "
                   "itself. One pass instead of trying every pair.",
    },
    "hash.group_key": {
        "name": "Grouping by a computed key",
        "explain": "When items belong together because they share something you can compute (first and last letter, "
                   "sorted letters, `r - c` for a diagonal), use that as a dict key: "
                   "`groups.setdefault(key(x), []).append(x)`. The skill is choosing the key.",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/1_foundations/04_hashing/group_by_ends.py`:

```python
"""
Group by First and Last Letter                                                [easy]

Group the words that start with the same letter AND end with the same letter.
Return the groups in the order their first word appears, with each group's
words in their original order. Words are lowercase and never empty.

Example:
    group_by_ends(["tab", "toast", "bat", "tilt", "bib", "top"])
        ->  [["tab"], ["toast", "tilt"], ["bat"], ["bib"], ["top"]]

Aim for:  O(n), one pass with a dict.
Hint:     Every word in a group shares the pair (first letter, last letter), so use
          (w[0], w[-1]) as a dict key and append each word to its key's list. A dict
          keeps its keys in the order they were added, so list(groups.values()) is
          already in the right order.
"""


def group_by_ends(words: list[str]) -> list[list[str]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["hash.group_key"]
USES = []

TESTS = [
    ((["tab", "toast", "bat", "tilt", "bib", "top"],), [["tab"], ["toast", "tilt"], ["bat"], ["bib"], ["top"]]),
    ((["a", "aa", "ab", "ba", "a"],), [["a", "aa", "a"], ["ab"], ["ba"]]),
    (([],), []),
    ((["cat"],), [["cat"]]),
    ((["dog", "dig", "dug"],), [["dog", "dig", "dug"]]),
]
```

  Create `solutions/group_by_ends.py`:

```python
def group_by_ends(words: list[str]) -> list[list[str]]:
    # The key is what every word in a group shares. Dicts keep insertion order. O(n).
    groups = {}
    for w in words:
        groups.setdefault((w[0], w[-1]), []).append(w)
    return list(groups.values())
```

- [ ] **Step 5: The new hard.** Create `course/1_foundations/04_hashing/grid_illumination.py`:

```python
"""
Grid Illumination                                                             [hard]

An n x n grid has lamps at the cells in `lamps`. A cell can be listed more than
once; it's still one lamp. A lamp lights every cell in its row, its column and
both of its diagonals. For each query [r, c], in order:

  1. answer 1 if cell (r, c) is lit, else 0;
  2. then turn off every lamp in the 3 x 3 block centred on (r, c).

Return the answers. n can be 1,000,000,000, with 20,000 lamps and 20,000
queries, so you can't build the grid or check every lamp for every query.

Example:
    grid_illumination(5, [[0, 0], [4, 4]], [[1, 1], [1, 0]])  ->  [1, 0]
        (1, 1) is on the diagonal of both lamps: lit. Then the lamp at (0, 0) goes off.
        (1, 0) shares no row, column or diagonal with the lamp left at (4, 4): dark.

Aim for:  O(lamps + queries).
Hint:     All cells on one diagonal share r - c, and on the other diagonal r + c. Keep four
          dicts that count the lamps on each row, column, r - c and r + c, plus a set of the
          lamps that are on. A cell is lit if any of its four counts is above 0. Turning a
          lamp off means removing it from the set and taking 1 off each of its four counts.
"""


def grid_illumination(n: int, lamps: list[list[int]], queries: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, lamps, queries):
    on = {tuple(lamp) for lamp in lamps}
    out = []
    for r, c in queries:
        out.append(int(any(a == r or b == c or a - b == r - c or a + b == r + c for a, b in on)))
        on = {(a, b) for a, b in on if max(abs(a - r), abs(b - c)) > 1}
    return out


def _fast(n, lamps, queries):
    on = {tuple(lamp) for lamp in lamps}
    lines = {}
    for r, c in on:
        for key in (("row", r), ("col", c), ("diag", r - c), ("anti", r + c)):
            lines[key] = lines.get(key, 0) + 1
    out = []
    for r, c in queries:
        out.append(int(any(lines.get(k, 0) for k in (("row", r), ("col", c), ("diag", r - c), ("anti", r + c)))))
        for a in (r - 1, r, r + 1):
            for b in (c - 1, c, c + 1):
                if (a, b) in on:
                    on.remove((a, b))
                    for key in (("row", a), ("col", b), ("diag", a - b), ("anti", a + b)):
                        lines[key] -= 1
    return out


def _cases():
    import random
    rng = random.Random(1001)
    out = []
    for _ in range(8):
        n = rng.randint(1, 8)
        lamps = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 8))]
        queries = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(1, 8))]
        out.append(((n, lamps, queries), _brute(n, lamps, queries)))
    lamps = [[rng.randrange(3000), rng.randrange(3000)] for _ in range(20_000)]
    queries = [[rng.randrange(3000), rng.randrange(3000)] for _ in range(20_000)]
    out.append(((1_000_000_000, lamps, queries), _fast(1_000_000_000, lamps, queries)))
    return out


USES = ["hash.group_key", "hash.set_lookup"]

TESTS = [
    ((5, [[0, 0], [4, 4]], [[1, 1], [1, 0]]), [1, 0]),
    ((5, [[0, 0], [4, 4]], [[1, 1], [1, 1]]), [1, 1]),
    ((5, [[0, 0], [0, 4]], [[0, 4], [0, 1], [1, 4]]), [1, 1, 0]),
    ((1, [[0, 0], [0, 0]], [[0, 0], [0, 0]]), [1, 0]),
    ((3, [], [[1, 1]]), [0]),
    ((6, [[2, 3], [2, 3]], [[0, 0], [2, 2], [5, 0]]), [0, 1, 0]),
] + _cases()
```

  Create `solutions/grid_illumination.py`:

```python
def grid_illumination(n: int, lamps: list[list[int]], queries: list[list[int]]) -> list[int]:
    # Count lamps per row, column and diagonal (r - c and r + c identify the two diagonals).
    # A query looks up four counts; switching a lamp off takes 1 off each. O(lamps + queries).
    on = set()
    rows, cols, diag, anti = Counter(), Counter(), Counter(), Counter()
    for r, c in lamps:
        if (r, c) in on:
            continue                    # listed twice, still one lamp
        on.add((r, c))
        rows[r] += 1
        cols[c] += 1
        diag[r - c] += 1
        anti[r + c] += 1
    answer = []
    for r, c in queries:
        answer.append(1 if rows[r] or cols[c] or diag[r - c] or anti[r + c] else 0)
        for a in (r - 1, r, r + 1):
            for b in (c - 1, c, c + 1):
                if (a, b) in on:
                    on.remove((a, b))
                    rows[a] -= 1
                    cols[b] -= 1
                    diag[a - b] -= 1
                    anti[a + b] -= 1
    return answer
```

- [ ] **Step 6: `is_happy`'s reference uses the seen set.** Its tags say it uses the seen set, and
  its hint offers that first. The current reference uses Floyd's fast and slow pointers, which the
  Linked lists topic (14) teaches. Replace `solutions/is_happy.py` with:

```python
def is_happy(n: int) -> bool:
    def step(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    seen = set()                        # a number we've met before means we're going round a loop
    while n != 1 and n not in seen:
        seen.add(n)
        n = step(n)
    return n == 1

    # No set needed (Linked lists topic): Floyd's fast and slow pointers. Move slow one step and
    # fast two; the number is happy if fast reaches 1, and loops if fast catches up with slow.
```

- [ ] **Step 7: Tag.**

```bash
python <workspace>/tag.py course/1_foundations/04_hashing first_repeat=:hash.seen_set longest_consecutive=hash.set_lookup:hash.run_starts contains_duplicate=hash.seen_set is_happy=hash.seen_set two_sum=:hash.complement valid_anagram= encode_decode= group_anagrams=hash.group_key top_k_frequent= is_valid_sudoku=hash.seen_set max_equal_freq= word_index=hash.set_lookup
```

  Expected: 12 `tagged` lines.

- [ ] **Step 8: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 9: Run** `python server.py --check 04_ coverage`. Expected: 14 `ok` lines;
  `ok   technique coverage … 24 techniques, 325 problem(s) not audited yet`; `All good.`

- [ ] **Step 10: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 1 audit: topic 04 tagged, with group_by_ends and grid_illumination" -m "Grouping by a computed key gets a basic problem. grid_illumination keeps two hard problems in Hashing after two moved out. is_happy's reference now uses the seen set it is tagged with." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Topic 05

**Files:**
- Modify: `course/techniques.py` (3 entries)
- Create: `course/1_foundations/05_recursion/min_max_expr.py`, `solutions/min_max_expr.py`
- Modify: every other file in `05_recursion/` (tags)
- Modify: `tests/test_coverage.py`

**Interfaces:**
- Consumes: `Stage1Audit`, `tag.py` (Task 1).
- Produces: `recursion.trust`, `recursion.memo`, `recursion.parse`; `min_max_expr` (title "Nested
  Min and Max"), which Task 6's browser check opens.

- [ ] **Step 1: Write the failing test.** Add to `Stage1Audit`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `test_topic_05` fails on unaudited problems.

- [ ] **Step 3: Registry.** In `course/techniques.py`, insert directly above `    "grid.neighbors": {`:

```python
    "recursion.trust": {
        "name": "Base case and a smaller call",
        "explain": "Answer the smallest input directly: that's the base case. For anything bigger, call the function "
                   "on a smaller piece, trust it to be right, and build your answer from it. Every call must move "
                   "toward the base case.",
    },
    "recursion.memo": {
        "name": "Memoisation",
        "explain": "When a recursive function is called again and again with the same arguments, remember each "
                   "answer: put `@cache` above it, or keep a dict. Each distinct call is then worked out once, which "
                   "can turn exponential time into the number of distinct calls.",
    },
    "recursion.parse": {
        "name": "Parsing with recursion",
        "explain": "Write `parse(i)` that reads the piece of text starting at index i and returns (its value, the "
                   "index just after it). When it meets an opening bracket, it calls itself for the inside and "
                   "carries on from the index that call returns.",
    },
```

- [ ] **Step 4: The new teacher.** Create `course/1_foundations/05_recursion/min_max_expr.py`:

```python
"""
Nested Min and Max                                                            [easy]

`expr` is either a whole number, or max(...) or min(...) around a list of
expressions separated by commas, nested as deep as you like. There are no
spaces. Return its value.

Example:
    min_max_expr("max(1,min(4,2),3)")       ->  3       min(4,2) is 2, then max(1,2,3) is 3
    min_max_expr("min(max(1,9),max(4,5))")  ->  5
    min_max_expr("7")                       ->  7

Aim for:  O(len(expr)): read each character once.
Hint:     Write parse(i): it reads the expression that starts at expr[i] and returns
          (its value, the index just after it). A digit: read the whole number. "max(" or
          "min(": skip those 4 characters, then call parse for each argument, stepping over
          the "," between them. At the ")", return the max or min and the index after it.
"""


def min_max_expr(expr: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["recursion.parse"]
USES = ["recursion.trust"]

TESTS = [
    (("max(1,min(4,2),3)",), 3),
    (("7",), 7),
    (("min(max(1,9),max(4,5))",), 5),
    (("max(10,2)",), 10),
    (("min(3)",), 3),
    (("max(min(5,max(6,7)),4,min(9,8))",), 8),
    (("min(max(0,0),12,max(min(30,40),25))",), 0),
    (("max(" * 50 + "1" + ")" * 50,), 1),
]
```

  Create `solutions/min_max_expr.py`:

```python
def min_max_expr(expr: str) -> int:
    def parse(i):
        """Value of the expression starting at expr[i], and the index just after it."""
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            return int(expr[i:j]), j
        pick = max if expr.startswith("max", i) else min
        i += 4                          # skip "max(" or "min("
        values = []
        while True:
            value, i = parse(i)         # trust the call for the inner expression
            values.append(value)
            if expr[i] == ")":
                return pick(values), i + 1
            i += 1                      # skip the ","

    return parse(0)[0]
```

- [ ] **Step 5: Tag.**

```bash
python <workspace>/tag.py course/1_foundations/05_recursion digit_sum=:recursion.trust count_paths=recursion.trust:recursion.memo flatten_list=recursion.trust power=recursion.trust calculate=recursion.parse,recursion.trust count_of_atoms=recursion.parse,recursion.trust scramble_string=recursion.memo,recursion.trust render_folders=recursion.trust
```

  Expected: 8 `tagged` lines.

- [ ] **Step 6: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 7: Run** `python server.py --check 05_ coverage`. Expected: 9 `ok` lines;
  `ok   technique coverage … 27 techniques, 317 problem(s) not audited yet`; `All good.`

- [ ] **Step 8: Commit**

```bash
git add course solutions tests/test_coverage.py
git commit -m "Stage 1 audit: topic 05 tagged, with min_max_expr" -m "Parsing with recursion gets a basic problem before calculate and count_of_atoms. count_paths already teaches memoisation, so scramble_string stays." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: README, browser check and full verification

**Files:**
- Modify: `README.md` (exercise count)
- Create: `tests/browser/stage_1.mjs`
- Modify: `tests/browser/README.md`

**Interfaces:**
- Consumes: everything above. Titles: "Best Time to Buy and Sell Stock" (`max_profit`), "Matching
  Pairs" (`equal_pairs`), "Nested Min and Max" (`min_max_expr`). Technique names from Tasks 2 and 5.

- [ ] **Step 1: README.** Replace `34 topics in 6 stages, 389 coding exercises` with
  `34 topics in 6 stages, 394 coding exercises` (389 plus the five new problems).

- [ ] **Step 2: Write the browser scenario.** Create `tests/browser/stage_1.mjs`:

```javascript
// Stage 1 audit on screen: topic 01's technique list, a moved teacher, the lock and banner it causes.
import { open, check, summary } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const text = (p, sel) => p.eval(`document.querySelector(${JSON.stringify(sel)})?.textContent || ""`);
const techList = (p) => p.eval(`[...document.querySelectorAll(".tech-list .item")].map(a => (a.classList.contains("solved") ? "✓" : "") + a.querySelector(".t").textContent)`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// Topic 01 lists its four techniques in teaching order.
await p.reload(BASE + "/#/t/01_big_o_in_practice");
const list = await techList(p);
check("topic 01 lists its techniques in teaching order",
  list.join(" | ") === "Set for fast lookups | Best so far | Counting pairs with a dict | Separating i from j", list.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve halvings", await solve(p, "halvings"));
check("solve common_count", await solve(p, "common_count"));

// The moved max_profit teaches Best so far.
await p.reload(BASE + "/#/p/max_profit");
check("max_profit shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Best so far");

// The hard is locked behind the new basic problem.
await p.reload(BASE + "/#/p/count_bad_pairs");
const lock = await text(p, ".reveal-box");
check("count_bad_pairs names the technique and its basic problem",
  lock.includes("This uses Counting pairs with a dict") && lock.includes("Matching Pairs teaches it"), lock);

// Progress follows the name: solving max_profit ticks Best so far on topic 01.
check("solve max_profit", await solve(p, "max_profit"));
await p.reload(BASE + "/#/t/01_big_o_in_practice");
check("solving max_profit ticks Best so far on topic 01", (await techList(p)).includes("✓Best so far"));

// A technique from an earlier topic shows a banner, not a lock.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve last_seen", await solve(p, "last_seen"));
check("solve word_frequencies", await solve(p, "word_frequencies"));
await p.reload(BASE + "/#/p/second_largest");
const banner = await text(p, ".tech-banner");
check("second_largest points back to topic 01", banner.includes("This uses Best so far") && banner.includes("Best Time to Buy and Sell Stock"), banner);

// The new recursion teacher, once 05's snippet and guided problem are solved.
check("solve digit_sum", await solve(p, "digit_sum"));
check("solve count_paths", await solve(p, "count_paths"));
await p.reload(BASE + "/#/p/min_max_expr");
check("min_max_expr shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Parsing with recursion");

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
```

- [ ] **Step 3: Mention it.** In `tests/browser/README.md`, after the line
  `    bash tests/browser/fresh.sh 8170 technique_coverage.mjs`, add a line
  `    bash tests/browser/fresh.sh 8171 stage_1.mjs`.

- [ ] **Step 4: Run** `node --check tests/browser/stage_1.mjs && bash tests/browser/fresh.sh 8171 stage_1.mjs`.
  Expected: every check passes (14 in all).

  If "topic 01 lists its techniques in teaching order" fails only on order, compare with
  `items` for topic 01 from `server.load_course()`. The list follows the ladder: rank, then
  same-rank teaching depth, then title. Fix the expectation only if the ladder order is right.

- [ ] **Step 5: Part 1's scenario still passes.** Run `bash tests/browser/fresh.sh 8170 technique_coverage.mjs`.
  Expected: 23 of 23 pass.

- [ ] **Step 6: Phase 1 still works.** Phase 1's scenarios live in this session's scratchpad
  (`scratchpad/cdp/t4.mjs` … `t8.mjs`); run each with `bash fresh.sh <port> tN.mjs` from that folder.
  Expected: 54 checks pass in total. Topic 01 gained two problems (`max_profit`, `equal_pairs`); a
  check that pins topic 01's problem list or count is updated to the new list, and each such
  change gets a ledger ruling. If the scratchpad is gone, check by hand: the first visit opens
  "Where are you starting?", and the Today card, "Placed out" tags and the how-to card appear.

- [ ] **Step 7: Unit tests.** Run `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 8: The whole course.** Run `python server.py --check`. Expected: every problem `ok`
  (394), `ok   starting check`, `ok   technique coverage … 27 techniques, 317 problem(s) not
  audited yet`, `All good.` This takes a few minutes.

- [ ] **Step 9: Commit**

```bash
git add README.md tests/browser/stage_1.mjs tests/browser/README.md
git commit -m "Stage 1 audit: README count and a browser check for topic 01's techniques" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
