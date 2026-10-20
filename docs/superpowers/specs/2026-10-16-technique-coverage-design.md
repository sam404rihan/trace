# Technique coverage: never meet a technique for the first time inside a problem

**Status:** draft for review, 2026-10-16.
**Scope:** two parts, each with its own implementation plan:

1. **Machinery.** A technique registry, per-problem tags, a coverage check, and the learner-facing
   pieces (the "New technique" box, the "Uses" row, locks and links). Graph traversal is the pilot
   and is fully audited as part of this.
2. **Content audit.** Tag every problem, then fix every gap the check reports, stage by stage.

## The problem

A topic's drills and guided problem teach the plain version of an idea. Its medium and hard
problems then quietly rely on other versions. If you know one kind of BFS, you can't solve a
problem that needs a different kind, and nothing tells you that's why you're stuck.

A first pass over all 383 problems (reading each problem's hint) found three kinds of gap. The
audit in Part 2 confirms and completes this list.

**1. Variants with no basic problem**

| Topic | Variant | Problems that rely on it |
|---|---|---|
| 19 Graph traversal | multi-source BFS (every start in the queue at once) | `rotting_oranges` |
| | flood fill from the border inward | `pacific_atlantic`, `surrounded_regions` |
| | BFS whose state is more than a cell, e.g. (cell, keys held) | `shortest_path_all_keys` |
| | BFS over a graph you build first (word patterns, buses) | `word_ladder`, `bus_routes` |
| 07 Sliding window | "exactly k" = at-most-k minus at-most-(k − 1) | `subarrays_k_distinct` (fixed: the new `nice_subarrays` teaches it) |
| 14 Linked lists | finding where a cycle starts (`has_cycle` only detects one) | `find_duplicate` (fixed: the new `cycle_start` teaches it) |
| 17 Heaps | two heaps for the median | `median_finder`, `sliding_window_median` (fixed: `median_finder`, now easy, teaches it) |
| | lazy deletion | `sliding_window_median`, `skyline`, `task_scheduler` (fixed: the new `max_bag` teaches it) |
| 21 Weighted graphs | Prim's minimum spanning tree | `min_cost_connect_points` |
| | Dijkstra on the worst step of a path ("bottleneck") | `swim_rising_water` |
| | Euler path (Hierholzer) | `reconstruct_itinerary` |
| | DP over (time, node) states | `min_cost_in_time` |
| 24 DP 2D | interval DP | `burst_balloons` |
| | two walkers at once | `cherry_pickup_ii` |
| | DP run backwards from the goal | `dungeon_game` |
| | memoised DFS on a grid | `longest_increasing_path` |
| 25 Bit tricks | DP over bitmasks | `min_xor_sum` |
| | building an answer bit by bit with prefixes | `max_xor_pair` |

**2. Problems that rely on a later topic**

| Problem (topic) | Needs | Taught in |
|---|---|---|
| `min_k_bit_flips` (03) | the forced first flip, and a difference array for where flips end | 08 and 11 (fixed: moved to 11) |
| `concat_all_words` (04) | sliding window | 07 (fixed: moved there) |
| `submatrix_sum_target` (04) | prefix sums + a dict of counts | 08 (fixed: moved there) |
| `scramble_string` (05) | memoisation | 23 DP (fixed: `count_paths`, 05's guided problem, already teaches it) |
| `split_array_largest_sum` (09) | a greedy feasibility check | 11 Greedy (fixed: `ship_capacity`, 09's guided problem, already teaches the same check) |
| `min_meeting_rooms`, `min_interval_query` (10) | heaps | 17 (fixed: moved there) |
| `word_search_ii` (18) | grid DFS + backtracking | 19, 22 (fixed: moved there) |
| `concatenated_words` (18) | DP | 23 (fixed: moved there) |
| `shortest_path_all_keys` (19) | bitmasks | 25 |
| `largest_factor_component` (20) | prime factorisation | 30 Number theory |

**3. Basic versions sorted after their users.** Problems of the same difficulty are ordered by
title, which is arbitrary for teaching. In Queues, the monotonic-deque problem
`sliding_window_max` (hard) comes after `max_value_of_equation` and `shortest_subarray_at_least_k`,
which both rely on it. Fixed in Stage 3: `sliding_window_max` is now the easy problem that teaches the
monotonic deque.

## Goal

Following the ladder in order, a learner meets every technique first in a **basic problem that
explains it and is built around it**, before any problem relies on it.

When a learner jumps ahead (Ctrl+K, a study plan, "Open anyway"), Trace says exactly which
techniques the problem uses and which basic problem teaches each one they haven't done.

## Assumptions

- **What "covered" means.** You didn't pick an option, so this spec uses option A: before a problem
  relies on a technique, there is a basic problem built around it, and that problem explains it.
  Option C (also a walkthrough layer) can come later through Phase 4's walkthroughs.
- All 34 topics, including Stage 0 when it exists.
- Both within-topic variants and techniques borrowed from other topics.
- A technique is a reusable idea a learner can know or not know, such as "multi-source BFS". Plain
  Python features (a dict, a slice) are not techniques here; the toolkit topic and Stage 0 cover
  those.
- Locks stay soft, as everywhere in Trace: "Open anyway" always works.

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

## Why

- **Mastery learning:** move on once the earlier step is solid. It raised exam scores across 108
  studies, most for weaker students (Kulik, Kulik & Bangert-Drowns 1990). A hidden variant is an
  earlier step that was never there.
- **Teach the pattern, then write with it:** comprehending a reusable pattern before writing code
  with it is an explicit step in Xie et al.'s (2019) theory of instruction. Teaching skills
  incrementally improved completion, errors and post-test understanding.
- **Beginners learn new techniques best from worked, focused examples,** not by discovering them
  inside a hard problem (the worked-example and expertise-reversal effects).
- **Prerequisite graphs:** Math Academy builds its course as a graph of which skills need which,
  and only serves a skill once its prerequisites are learned (the developer's account, not an
  independent evaluation).

## Design

### The registry: `course/techniques.py`

Plain Python data, validated by the server like walkthroughs. One entry per technique: a name and a
short explanation (2–4 sentences, inline code allowed). This is the single source of the
explanation. The teaching problem shows it, and so does every "Uses" chip.

```python
"""Every technique a problem may rely on. Each is taught by exactly one basic problem
(the one that lists it in TEACHES), before any problem that lists it in USES."""

TECHNIQUES = {
    "bfs.grid": {
        "name": "BFS on a grid",
        "explain": "Each cell is a node and its neighbours are the 4 cells around it. A queue hands out "
                   "cells in order of distance, so the first time you reach a cell is along a shortest path.",
    },
    "bfs.multi_source": {
        "name": "Multi-source BFS",
        "explain": "Put every starting cell in the queue at distance 0 before the loop begins. The ripple "
                   "then spreads from all of them at once, so each cell's distance is to its nearest start.",
    },
    # ...
}
```

Ids are `<area>.<variant>`, lowercase, for example `bfs.state`, `window.at_most_k`,
`heap.lazy_delete` or `dp.interval`.

### Tags in problem files

```python
TEACHES = ["bfs.multi_source"]     # this is the basic problem for these techniques (it uses them too)
USES = ["bfs.grid"]                # other techniques this problem needs, each taught before it
```

- Every problem gets `USES`, which may be empty. It lists every technique the problem uses
  directly, including basic ones like grid neighbours, not just the newest one. That way the
  "Uses" row shows everything the problem relies on.
- `USES` lists techniques in teaching order, the order their teachers come in the course, so the
  lock names the first basic problem to do.
- A problem with neither field counts as **not yet audited**.
- Basic problems also get `TEACHES`.
- The server reads both fields in `parse_problem`, the way it reads `TESTS` and `STEPS`.

### What a teaching problem looks like

- Kind `snippet`, `guided` or `easy` (`parsons` once Phase 4 adds it).
- Built around the one technique, with small inputs.
- The statement shows a **"New technique: <name>"** box above it, with the registry's explanation.
- Its hint and reference solution use the technique in its plainest form.
- Its big test times out for the naive solution a learner without the technique would write. The
  exceptions are techniques that save only space, or whose naive version is slow only on inputs
  too deep to test; each stage plan lists them.

### The coverage rules

Course order means topics in order. Within a topic, problems are sorted by ladder rank (snippet 0,
guided 1, easy 2, medium 3, hard 4, build 5). Within a rank, a problem goes after every same-topic
problem that teaches a technique it uses, then the rest are sorted by title. So a chain of basics,
such as an easy problem that needs flood fill from another easy problem, comes out in teaching
order. The server sorts this way and the check uses the same order. The check enforces these
rules:

1. Every id in `USES` or `TEACHES` exists in the registry.
2. Every registry technique has exactly one teacher.
3. A teacher's kind is `snippet`, `guided` or `easy` (or `parsons`).
4. For every problem P and every technique t in P's `USES`, t's teacher comes **before** P in
   course order: in an earlier topic, or earlier in the same topic. A dependency cycle always
   breaks this rule, so the check catches cycles too.
   Rule 4 applies to teachers' own `USES` as well, so every chain of prerequisites is valid.
5. No problem lists the same id in both `TEACHES` and `USES`.
6. **Audit progress.** A problem that isn't audited yet produces a warning, not a failure. Once
   Part 2 finishes, unaudited problems become failures too.

### The check

New `coverage.py`: a pure function `check_coverage(topics, problems, techniques) -> (errors,
warnings)`, which returns plain-English lines that name the problem, the technique and the rule.
For example: "rotting_oranges uses bfs.multi_source, but its teacher comes later in the same topic".

- `python server.py --check` runs it and fails on any error. Warnings are printed with a count
  ("212 problems not yet audited").
- A unit test runs it on the real course and requires zero errors. Once Part 2 finishes, it also
  requires zero warnings.
- `server.py` loads the registry with a `parse_techniques()` that validates its shape, and
  `/api/course` adds `"techniques": {id: {"name", "explain", "teacher"}}`. Each problem summary
  gains `"uses"` and `"teaches"`.

### What the learner sees

New `web/techniques.js`, so `app.js` doesn't grow.

- **On a teaching problem:** the "New technique" box above the statement.
- **On every problem:** a **"Uses"** row under the title, with one chip per technique. A chip shows
  ✓ when its teacher is solved. Clicking a chip opens its explanation, with a link to the teacher
  problem.
- **A soft lock within a topic.** If a problem uses a technique whose teacher is in the same topic
  and still unsolved, the problem is locked. The message names the problem to do first: "This uses
  multi-source BFS. Spreading fire teaches it; do that one first." "Go to Spreading fire" and "Open
  anyway" are both there.
  - This extends the existing ladder rule in `blocker()`; solo problems still need the snippet and
    the guided problem as well.
  - It doesn't apply to placed-out topics or in study-plan mode, which already skip locks.
- **A banner for other topics.** If the teacher is in another topic and unsolved, a banner says
  "This uses sliding window (topic 07). If it's new to you, try Max sum of k in a row first."
  There's no lock, so a learner working in one topic isn't blocked by another.
- **A technique counts as known** when its teacher is solved or the teacher's topic is placed out.
  That decides the ✓, the lock and the banner.
- **On the topic page:** a **"Techniques in this topic"** list, in teaching order. Each item has its
  name, a ✓ when learned, and a link to its teaching problem. This answers "which kinds of BFS are
  there?" at a glance.

### Fixing a gap

When the check reports a problem, fix it with the first of these that fits:

1. **Reuse an existing basic problem** that already fits the technique. Add `TEACHES`, write the
   explanation, and adjust the problem if needed.
2. **Move the problem** to the topic where its last prerequisite is taught, when it naturally
   belongs there. For example, `min_meeting_rooms` moves to Heaps and `word_search_ii` to
   Backtracking.
   - Problem names don't change, so progress, saved code and study plans are unaffected.
   - Solutions are keyed by name in `solutions/`, so they don't move.
3. **Write a new basic problem** for the technique: an easy (or snippet) problem with small tests,
   a reference solution, and the explanation in the registry.
4. **Simplify the problem** so it no longer needs the technique, but only when the technique isn't
   the point of the problem.

Expect roughly 40–70 new basic problems in all. The audit gives the real number. For the pilot
topic, Graph traversal, the pilot audit found five, plus one re-ranked problem (see Part 1).

## How it fits the other phases

- **Phase 1 placement:** a placed-out topic's techniques count as known, so its in-topic locks stay
  off. That matches Phase 1's "everything stays open".
- **Phase 2 mixed practice:** the "Uses" row and the banner name the technique, so mixed mode hides
  them along with the title and topic. Phase 2's plan must add them to its hide list.
- **Phase 3 help:** the "I don't know how to start" choice can show the explanations of the
  problem's techniques, straight from the registry.
- **Phase 4:** Stage 0 problems get tagged as well, and the new `parsons` kind may teach.
- **Order:** this work doesn't depend on Phases 2–4, and it fixes the most basic promise of every
  problem. Doing it before Phase 2 means reviews and mixed sets are built on problems with no hidden
  prerequisites.

## Part 1: machinery and the Graph traversal pilot

**What it delivers:**
- the registry format and loader;
- `USES`/`TEACHES` parsing;
- `coverage.py`, wired into `--check` and a unit test;
- the API fields;
- the box, the chips, the lock, the banner and the topic list;
- Graph traversal fully audited and fixed. That means its techniques in the registry, every problem
  tagged, and its gaps fixed. The pilot audit found that multi-source BFS is already taught by the
  guided problem `distance_to_exit`. Five techniques get new easy problems: graph traversal from
  edges or node links, searching back from the targets, BFS with generated neighbours, BFS over a
  richer state, and rebuilding a path from parents. `num_islands` is re-ranked to easy so it can
  teach counting connected regions. `shortest_path_all_keys` holds its keys in a set, not a
  bitmask, so it no longer depends on Bit tricks (topic 25).

**Tests:**
- `tests/test_coverage.py` builds small fake courses. Each one tests a single rule: unknown id, no
  teacher or two teachers, a teacher of the wrong kind, a teacher later in the same topic, a teacher in a
  later topic, a cross-topic teacher in an earlier topic (allowed), a teacher with a bad chain, the
  same id taught and used, and an unaudited problem giving a warning only.
- A real-course test: zero errors across the course, and zero warnings in Graph traversal.
- `--check` passes, including the five new problems' solutions and starters.
- Browser checks (headless, as in Phase 1):
  - the box on a teaching problem;
  - chips with ✓ and without;
  - the in-topic lock and "Open anyway";
  - the banner for a teacher in another topic;
  - no lock in study-plan mode or on a placed-out topic;
  - the topic page's technique list.

## Part 2: the content audit

One plan per stage (Stages 1–6, then Stage 0 when Phase 4 adds it). For each topic:

1. Read every problem's statement, hint and reference solution. List the techniques it needs.
2. Add registry entries for the topic's techniques.
3. Tag every problem with `USES`, and `TEACHES` on teachers.
4. Run `--check` and fix each error in the order given in "Fixing a gap".
5. Update the README's counts if problems were added or moved.

Cross-topic dependencies are fixed in the earlier topic, by moving the problem or teaching the
basic earlier. A technique from a later topic is never allowed.

When the last stage is done, rule 6 turns strict: the unit test requires zero unaudited problems.

## Success criteria

- `python server.py --check` reports zero coverage errors, and after Part 2, zero unaudited
  problems.
- Every registry technique has exactly one basic teaching problem with an explanation.
- Following the ladder in order, no problem uses a technique whose teacher you haven't been offered
  first.
- On any problem, the "Uses" row shows every technique it relies on, and each unlearned one links
  to its teacher.
- Graph traversal (Part 1) has a basic problem for every technique its problems use, each before
  the problems that need it.

## Left out

- **Working out techniques automatically from code.** Deciding which techniques a solution needs
  is a judgment call; tags are written by hand and checked by rules.
- **Hard locks** across topics or for study plans: against Trace's soft-lock design. The banner
  covers jumping ahead.
- **Several teachers per technique** (an easy and a walkthrough). One teacher keeps the rules
  simple. Walkthroughs can point at the teacher.
- **An explicit ordering field** (an `ORDER` list). Sorting by teaching dependencies gives the
  order automatically.

## References

- Kulik, Kulik & Bangert-Drowns 1990, mastery learning: [record](https://www.academia.edu/81783373/Effectiveness_of_Mastery_Learning_Programs_A_Meta_Analysis)
- Xie et al. 2019, a theory of instruction for programming (templates, incremental skills): [PDF](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)
- Expertise reversal effect: [overview](https://en.wikipedia.org/wiki/Expertise_reversal_effect)
- Math Academy (Skycak), prerequisite graph and spaced review: [article](https://justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/)
- The beginner-path spec (Phases 1–4): `docs/superpowers/specs/2026-10-16-beginner-path-design.md`
