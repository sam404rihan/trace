# Technique coverage, Part 2 Stage 6: audit topics 30–34 and turn the check strict — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem in the course lists the techniques it uses, each taught earlier by a basic
problem, and from now on an untagged problem is a coverage error, not a warning.

**Architecture:** Content work for topics 30–34, then one small code change. 17 techniques join
`course/techniques.py` (117 in all). Every Stage 6 problem gets `USES` (and `TEACHES` on
teachers), including `largest_factor_component`, which Stage 4 moved in. One new easy teacher is
added (`prime_factors`), and five problems are re-ranked to easy. Then `technique_coverage.py`
reports an unaudited problem as an error, as the spec's rule 6 says it should once Part 2 ends.

**Tech Stack:** Python 3.12 stdlib, `unittest`, `--check`, the Node headless-Chrome scenarios, and
`runner/judge.py` on the bundled Python for shortcut timing.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md` (rule 6: "Once Part 2
finishes, unaudited problems become failures too"). The Stage 5 plan is the model; its Global
Constraints still apply.

## Global Constraints

- No new dependencies. Names, topic ids and drill keys never change.
- Tags go directly above `TESTS =`. `USES` is in teaching order (`test_uses_are_in_teaching_order`).
- One teacher per technique (a snippet, guided or easy problem), before every user. Nothing from a
  later topic. At least two hards per topic. Headers are 84 wide. Line endings are kept.
- A teacher's big test must time out (2 s) for the naive solution a learner without the technique
  would write. These were run through the real judge while this plan was written:
  - `prime_factors`: trying every number up to n times out on 999,999,999,989; the reference takes 82 ms.
  - `lca_queries`: walking up parent by parent times out.
  - `min_edge_reversals`: a BFS from every node times out.
  - `subtree_sizes`: plain recursion fails on its 100,000-node path, past Python's recursion limit.
- **Exceptions in this stage:**
  - `polygon_area`: any correct method is the shoelace formula or a triangle fan that equals it.
  - `max_staffing` and `min_cut_edges`: the natural alternatives, assigning or cutting greedily, are
    wrong rather than slow. Task 4 checks a greedy version against their tests.
- `TAG` is the Stage 2 helper: `C:/Users/sam/AppData/Local/Temp/claude/C--Users-sam-Desktop-dsa/37698c59-d18f-494f-9d0b-cad64d5356c4/scratchpad/s2/tag.py`.
- End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Audit results

**New techniques (17), in course order:**

| Id | Name | Teacher | How the gap is fixed |
|---|---|---|---|
| `nt.fast_pow` | Fast power by squaring | `mod_pow` (snippet, 30) | reuse |
| `nt.sieve` | Sieve of Eratosthenes | `count_primes` (guided, 30) | reuse |
| `nt.mod_inverse` | Dividing modulo m | `extended_gcd` | **re-rank** medium → easy; `binomials` and `chinese_remainder` rely on it |
| `nt.trial_division` | Factoring by trial division | `prime_factors` | **new** easy in 30: `euler_phi` and `largest_factor_component` rely on it |
| `geo.cross` | The cross product for turns | `orientation` (snippet, 31) | reuse |
| `geo.hull` | Convex hull (monotone chain) | `convex_hull` (guided, 31) | reuse |
| `geo.shoelace` | The shoelace formula | `polygon_area` (easy, 31) | reuse; `fence_planner` relies on it |
| `tree.lift_jump` | Jumping with a lifting table | `lift_jump` (snippet, 32) | reuse |
| `tree.lift_table` | Building a lifting table | `tree_ancestor` (guided, 32) | reuse |
| `tree.bfs_order` | Bottom-up without recursion | `subtree_sizes` (easy, 32) | reuse; five problems in 32 rely on it |
| `tree.lca` | Lowest common ancestor with lifting | `lca_queries` | **re-rank** medium → easy; `path_weight_queries` and `family_tree` rely on it |
| `tree.reroot` | Rerooting | `min_edge_reversals` | **re-rank** hard → easy: the plainest rerooting (each edge costs 0 or 1); `sum_of_distances` relies on it |
| `flow.augment` | Max flow by augmenting paths | `max_flow` (guided, 33) | reuse |
| `flow.min_cut` | The minimum cut | `min_cut_edges` | **re-rank** hard → easy; `project_selection` relies on it |
| `flow.model` | Modelling a problem as flow | `max_staffing` | **re-rank** medium → easy; `project_selection` and `schedule_interviews` rely on it |
| `dp.digit` | Digit DP | `digit_choices` (snippet, 34) | reuse |
| `dp.digit_started` | Leading zeros in digit DP | `count_without_digit` (guided, 34) | reuse |

Everything else in 30–34 is a hard's own insight, or builds on techniques from earlier stages.
After the re-ranks, topic 32 keeps 2 hards (`path_weight_queries`, `sum_of_distances`) and topic 33
keeps 2 (`min_cost_flow`, `project_selection`).

**Tags for every problem.** USES is in teaching order.

| Topic | Problem | TEACHES | USES | Notes |
|---|---|---|---|---|
| 30 | `mod_pow` (snippet) | `nt.fast_pow` | `bits.shift_mask` | |
| 30 | `count_primes` (guided) | `nt.sieve` | | |
| 30 | `extended_gcd` (now easy) | `nt.mod_inverse` | | |
| 30 | `prime_factors` (new) | `nt.trial_division` | | |
| 30 | `trailing_zeroes` | | | own: count the 5s |
| 30 | `euler_phi` | | `nt.trial_division` | own: result -= result // p |
| 30 | `binomials` (hard) | | `nt.fast_pow`, `nt.mod_inverse` | own: factorial tables |
| 30 | `chinese_remainder` (hard) | | `nt.mod_inverse` | own: merge two conditions at a time |
| 30 | `factorize_all` (hard) | | `nt.sieve` | own: smallest prime factor table |
| 30 | `largest_factor_component` (hard, moved in) | | `uf.find`, `uf.union`, `nt.trial_division` | own: link numbers to their primes |
| 30 | `nth_magical_number` (hard) | | `bsearch.first_true`, `bsearch.on_answer` | own: inclusion-exclusion count |
| 30 | `evaluate_fraction` (build) | | `recursion.trust`, `recursion.parse` | own: reduce with gcd |
| 31 | `orientation` (snippet) | `geo.cross` | | |
| 31 | `convex_hull` (guided) | `geo.hull` | `geo.cross` | |
| 31 | `polygon_area` | `geo.shoelace` | `geo.cross` | |
| 31 | `segments_intersect`, `point_in_polygon` | | `geo.cross` | own: four touching cases; casting a ray |
| 31 | `closest_pair` (hard) | | `bsearch.first_true`, `window.variable` | own: only points within d in y |
| 31 | `max_points_on_line` (hard) | | `hash.group_key` | own: exact direction with gcd and sign |
| 31 | `rectangle_area_ii` (hard) | | `intervals.merge`, `intervals.sort_by_start` | own: sweep the x events |
| 31 | `fence_planner` (build) | | `geo.cross`, `geo.hull`, `geo.shoelace` | own: rebuild only for a post outside |
| 32 | `lift_jump` (snippet) | `tree.lift_jump` | `bits.shift_mask` | |
| 32 | `tree_ancestor` (guided) | `tree.lift_table` | `tree.lift_jump` | |
| 32 | `subtree_sizes` | `tree.bfs_order` | `graph.adjacency` | |
| 32 | `lca_queries` (now easy) | `tree.lca` | `tree.lift_jump`, `tree.lift_table`, `tree.bfs_order` | |
| 32 | `min_edge_reversals` (now easy) | `tree.reroot` | `tree.bfs_order` | |
| 32 | `tree_diameter` | | `bfs.shortest`, `graph.adjacency` | own: the farthest node is one end |
| 32 | `path_weight_queries` (hard) | | `prefix.sums`, `tree.lift_table`, `tree.lca` | own: weight counts from the root |
| 32 | `sum_of_distances` (hard) | | `tree.bfs_order`, `tree.reroot` | own: size[c] closer, n − size[c] farther |
| 32 | `family_tree` (build) | | `tree.lift_table`, `tree.bfs_order`, `tree.lca` | |
| 33 | `bottleneck` (snippet) | | | |
| 33 | `max_flow` (guided) | `flow.augment` | `bfs.shortest`, `bfs.path` | |
| 33 | `min_cut_edges` (now easy) | `flow.min_cut` | `flow.augment` | |
| 33 | `edge_disjoint_paths` | | `flow.augment` | own: capacity 1 per cable |
| 33 | `max_staffing` (now easy) | `flow.model` | `flow.augment` | |
| 33 | `max_matching` | | `recursion.trust`, `flow.augment` | own: Kuhn's "can the holder move?" |
| 33 | `min_cost_flow` (hard) | | `sp.bellman_ford`, `flow.augment` | own: cheapest path, refund edges |
| 33 | `project_selection` (hard) | | `flow.augment`, `flow.min_cut`, `flow.model` | own: profits from the source, costs to the sink |
| 33 | `schedule_interviews` (build) | | `flow.augment`, `flow.model` | own: slots in the middle |
| 34 | `digit_choices` (snippet) | `dp.digit` | | |
| 34 | `count_without_digit` (guided) | `dp.digit_started` | `recursion.memo`, `dp.digit` | |
| 34 | `jump_game_vi` | | `deque.monotonic`, `dp.recurrence` | |
| 34 | `count_digit_one` | | | own: count each position |
| 34 | `constrained_subset_sum` (hard) | | `greedy.kadane`, `deque.monotonic`, `dp.recurrence` | |
| 34 | `count_digit_sum_range` (hard) | | `recursion.memo`, `prefix.sums`, `dp.digit` | own: stop once the sum passes max |
| 34 | `count_stepping_numbers` (hard), `number_range` (build) | | `recursion.memo`, `prefix.sums`, `dp.digit`, `dp.digit_started` | own: the previous digit in the state; one helper for four questions |
| 34 | `at_most_n_given_digits` (hard) | | `dp.digit` | own: shorter numbers all fit |

## Review Focus

1. **The strict rule bites.** After Task 6, a problem with no `USES` makes `--check` fail. Owners:
   the Task 6 test `test_unaudited_is_an_error`, and `test_no_coverage_errors` on the real course.
2. **Teachers can't be passed by a shortcut**, apart from the listed exceptions. Owner: the Task 5
   test `test_teacher_big_tests_reject_the_naive_solution`, plus the judge runs above.
3. **Two hards per topic after five re-ranks.** Owner: the Task 5 test `test_every_stage_6_topic_keeps_two_hard_problems`.
4. **Nothing else reads the old warning list.** `--check` prints the coverage line without the
   "not audited yet" count, and nothing in `web/` depends on it. Owner: Task 6 Step 3 (grep), and
   the full `--check` in Task 7.
5. **Every problem in the course is audited.** Owner: `test_no_coverage_errors` once rule 6 is strict.

---

### Task 1: Topic 30, number theory

**Files:** `tests/test_coverage.py` (new `Stage6Audit`); `course/techniques.py` (4 entries); create
`30_number_theory/prime_factors.py` and its solution; `extended_gcd.py` (re-rank); every problem file (tags).

- [ ] **Step 1: Failing test** above `if __name__ == "__main__":`:

```python
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
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`: `test_topic_30` fails.
- [ ] **Step 3: Registry** (above `    "grid.neighbors": {`):

```python
    "nt.fast_pow": {
        "name": "Fast power by squaring",
        "explain": "To compute `base ** exp % mod`, walk the bits of exp from the lowest. Keep squaring the base "
                   "(mod mod), and multiply it into the result whenever the current bit is 1. That's O(log exp) "
                   "multiplications instead of exp. Python's `pow(base, exp, mod)` does the same.",
    },
    "nt.sieve": {
        "name": "Sieve of Eratosthenes",
        "explain": "To find every prime below n, start with all numbers marked prime. For each p from 2 while "
                   "p * p < n, if p is still marked, cross out p * p, p * p + p, ... Everything left marked is "
                   "prime. It's about O(n log log n), and the same loop can record each number's smallest prime factor.",
    },
    "nt.mod_inverse": {
        "name": "Dividing modulo m",
        "explain": "Dividing by b modulo m means multiplying by its inverse x, where `b * x % m == 1`. It exists "
                   "when gcd(b, m) == 1. Extended Euclid finds it from `b * x + m * y == 1`. When m is prime, "
                   "Fermat gives it directly: `pow(b, m - 2, m)`, and Python's `pow(b, -1, m)` works for any m.",
    },
    "nt.trial_division": {
        "name": "Factoring by trial division",
        "explain": "To factor n, try divisors d = 2, 3, 4, ... while d * d <= n, dividing each one out as often as it "
                   "goes in. Composite d never divide what's left, since their prime factors went first. Whatever is "
                   "left above 1 at the end is a prime factor bigger than the square root. It's O(sqrt(n)).",
    },
```

- [ ] **Step 4: New teacher** `course/6_specialist_topics/30_number_theory/prime_factors.py`:

```python
"""
Prime Factors                                                                 [easy]

Return the prime factors of n (2 <= n <= 10**12) in increasing order, each one
repeated as often as it divides n.

Example:
    prime_factors(360)  ->  [2, 2, 2, 3, 3, 5]
    prime_factors(97)   ->  [97]

Aim for:  O(sqrt(n)). The last tests are near 10**12: trying every number up to n times
          out, but trying divisors only up to the square root takes about a million steps.
Hint:     Trial division. Try d = 2, 3, 4, ... while d * d <= n. Whenever d divides n,
          record d, divide it out, and try the same d again. A composite d never divides
          what's left, because its own prime factors were divided out first. Whatever is
          left above 1 at the end is one more prime factor.
"""


def prime_factors(n: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["nt.trial_division"]
USES = []

TESTS = [
    ((360,), [2, 2, 2, 3, 3, 5]),
    ((97,), [97]),
    ((2,), [2]),
    ((1024,), [2] * 10),
    ((600_851_475_143,), [71, 839, 1471, 6857]),
    ((2 ** 39,), [2] * 39),
    ((999_979 * 999_983,), [999_979, 999_983]),
    ((999_999_999_989,), [999_999_999_989]),
]
```

  `solutions/prime_factors.py`:

```python
def prime_factors(n: int) -> list[int]:
    # Trial division up to sqrt(n): each prime is divided out as often as it goes in. O(sqrt(n)).
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)                   # one prime factor above the square root is left
    return factors
```

- [ ] **Step 5:** `extended_gcd`'s header becomes `[easy]`, 84 wide.
- [ ] **Step 6: Tag.**

```bash
python $TAG course/6_specialist_topics/30_number_theory mod_pow=bits.shift_mask:nt.fast_pow count_primes=:nt.sieve extended_gcd=:nt.mod_inverse trailing_zeroes= euler_phi=nt.trial_division binomials=nt.fast_pow,nt.mod_inverse chinese_remainder=nt.mod_inverse factorize_all=nt.sieve largest_factor_component=uf.find,uf.union,nt.trial_division nth_magical_number=bsearch.first_true,bsearch.on_answer evaluate_fraction=recursion.trust,recursion.parse
```

- [ ] **Step 7: Run** the unit tests and `--check 30_ coverage`: 12 `ok`; `104 techniques, 36 problem(s) not audited yet`.
- [ ] **Step 8: Commit** `Stage 6 audit: topic 30 tagged, with prime_factors`.

### Task 2: Topic 31, geometry

- [ ] **Step 1: Failing test:**

```python
    def test_topic_31(self):
        self.assert_audited("31_geometry")
        self.assert_teaches({"orientation": ["geo.cross"], "convex_hull": ["geo.hull"], "polygon_area": ["geo.shoelace"]})
        self.assert_uses({"fence_planner": ["geo.cross", "geo.hull", "geo.shoelace"],
                          "rectangle_area_ii": ["intervals.merge", "intervals.sort_by_start"],
                          "max_points_on_line": ["hash.group_key"], "segments_intersect": ["geo.cross"]})
```

- [ ] **Step 2: Run** it: `test_topic_31` fails.
- [ ] **Step 3: Registry:**

```python
    "geo.cross": {
        "name": "The cross product for turns",
        "explain": "For points p, q and r, `(q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)` is positive for a "
                   "left turn, negative for a right turn and 0 when they're on one line. It's exact with integers, so "
                   "there are no angles. r lies on segment pq when it's 0 and r is inside pq's bounding box.",
    },
    "geo.hull": {
        "name": "Convex hull (monotone chain)",
        "explain": "Sort the points. Walk left to right building the bottom chain: before adding a point, pop the "
                   "last one while the last two and the new point don't make a left turn. Do the same right to left "
                   "for the top chain, then join them. O(n log n) for the sort.",
    },
    "geo.shoelace": {
        "name": "The shoelace formula",
        "explain": "The area of a polygon whose corners are listed in order is half the absolute value of the sum, "
                   "over every edge (wrapping to the first corner), of `x[i] * y[i + 1] - x[i + 1] * y[i]`. Each term "
                   "is a signed triangle from the origin, and the parts outside the polygon cancel.",
    },
```

- [ ] **Step 4: Tag.**

```bash
python $TAG course/6_specialist_topics/31_geometry orientation=:geo.cross convex_hull=geo.cross:geo.hull polygon_area=geo.cross:geo.shoelace segments_intersect=geo.cross point_in_polygon=geo.cross closest_pair=bsearch.first_true,window.variable max_points_on_line=hash.group_key rectangle_area_ii=intervals.merge,intervals.sort_by_start fence_planner=geo.cross,geo.hull,geo.shoelace
```

- [ ] **Step 5: Run** the unit tests and `--check 31_ coverage`: 9 `ok`; `107 techniques, 27 problem(s) not audited yet`.
- [ ] **Step 6: Commit** `Stage 6 audit: topic 31 tagged`.

### Task 3: Topic 32, advanced trees

- [ ] **Step 1: Failing test:**

```python
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
```

- [ ] **Step 2: Run** it: `test_topic_32` fails.
- [ ] **Step 3: Registry:**

```python
    "tree.lift_jump": {
        "name": "Jumping with a lifting table",
        "explain": "With `up[j][v]` = the 2^j-th ancestor of v, the k-th ancestor is a few jumps: for every bit j set "
                   "in k, do `v = up[j][v]`. The jumps add up to exactly k, so it takes O(log k) steps instead of k.",
    },
    "tree.lift_table": {
        "name": "Building a lifting table",
        "explain": "Row 0 of the table is each node's parent. Each next row doubles the jump: "
                   "`up[j][v] = up[j - 1][up[j - 1][v]]`, the 2^(j-1)-th ancestor of the 2^(j-1)-th ancestor. About "
                   "log n rows cover any jump, in O(n log n) time and space.",
    },
    "tree.bfs_order": {
        "name": "Bottom-up without recursion",
        "explain": "Deep trees break recursion in Python. Instead, BFS from the root, recording each node's parent "
                   "and the order you visit them: every parent comes before its children. Walk that order BACKWARDS "
                   "to combine children into parents, or forwards to push values from parents down.",
    },
    "tree.lca": {
        "name": "Lowest common ancestor with lifting",
        "explain": "To find where u's and v's paths to the root meet, first lift the deeper one by the depth "
                   "difference. If they're now equal, that's the answer. Otherwise, from the biggest jump down, move "
                   "both up whenever their ancestors differ; the answer is then the parent of either. O(log n).",
    },
    "tree.reroot": {
        "name": "Rerooting",
        "explain": "To answer a question for every node as the root, solve it once for the root (one pass), then "
                   "move the root along each edge from parent to child. Usually only that edge's contribution "
                   "changes, so `answer[child]` comes from `answer[parent]` in O(1). Two passes in all: O(n).",
    },
```

- [ ] **Step 4:** The headers of `lca_queries` and `min_edge_reversals` become `[easy]`, 84 wide.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/6_specialist_topics/32_advanced_trees lift_jump=bits.shift_mask:tree.lift_jump tree_ancestor=tree.lift_jump:tree.lift_table subtree_sizes=graph.adjacency:tree.bfs_order lca_queries=tree.lift_jump,tree.lift_table,tree.bfs_order:tree.lca min_edge_reversals=tree.bfs_order:tree.reroot tree_diameter=bfs.shortest,graph.adjacency path_weight_queries=prefix.sums,tree.lift_table,tree.lca sum_of_distances=tree.bfs_order,tree.reroot family_tree=tree.lift_table,tree.bfs_order,tree.lca
```

- [ ] **Step 6: Run** the unit tests and `--check 32_ coverage`: 9 `ok`; `112 techniques, 18 problem(s) not audited yet`.
- [ ] **Step 7: Commit** `Stage 6 audit: topic 32 tagged`.

### Task 4: Topic 33, network flow

- [ ] **Step 1: Failing test:**

```python
    def test_topic_33(self):
        self.assert_audited("33_network_flow")
        self.assert_teaches({"max_flow": ["flow.augment"], "min_cut_edges": ["flow.min_cut"], "max_staffing": ["flow.model"]})
        self.assert_uses({"project_selection": ["flow.augment", "flow.min_cut", "flow.model"],
                          "min_cost_flow": ["sp.bellman_ford", "flow.augment"],
                          "schedule_interviews": ["flow.augment", "flow.model"]})
        for name in ("min_cut_edges", "max_staffing"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)
```

- [ ] **Step 2: Run** it: `test_topic_33` fails.
- [ ] **Step 3: Registry:**

```python
    "flow.augment": {
        "name": "Max flow by augmenting paths",
        "explain": "Keep the spare capacity of every edge, with a reverse edge that starts at 0. While BFS finds a "
                   "path from source to sink through spare capacity, push its smallest spare amount along it, taking "
                   "it off each edge and adding it to the reverse edge, so later paths can undo it.",
    },
    "flow.min_cut": {
        "name": "The minimum cut",
        "explain": "When max flow finishes, the nodes still reachable from the source through spare capacity are one "
                   "side of a cheapest cut. The full edges leaving that side form the cut, and their capacities add "
                   "up to exactly the max flow, so no cheaper way to separate source from sink exists.",
    },
    "flow.model": {
        "name": "Modelling a problem as flow",
        "explain": "Many assignment problems are a flow network: source → each person (capacity: how many they can "
                   "take) → each allowed choice (capacity 1) → sink (capacity: how many each choice needs). Each unit "
                   "of max flow is one assignment, and the capacities enforce every rule at once.",
    },
```

- [ ] **Step 4:** The headers of `min_cut_edges` and `max_staffing` become `[easy]`, 84 wide.
- [ ] **Step 5: Tag.**

```bash
python $TAG course/6_specialist_topics/33_network_flow bottleneck= max_flow=bfs.shortest,bfs.path:flow.augment edge_disjoint_paths=flow.augment max_matching=recursion.trust,flow.augment max_staffing=flow.augment:flow.model min_cut_edges=flow.augment:flow.min_cut min_cost_flow=sp.bellman_ford,flow.augment project_selection=flow.augment,flow.min_cut,flow.model schedule_interviews=flow.augment,flow.model
```

- [ ] **Step 6: The exception holds.** Run a greedy `max_staffing` through the judge: each worker takes
  their allowed projects in order while seats remain. It must fail at least one test.
- [ ] **Step 7: Run** the unit tests and `--check 33_ coverage`: 9 `ok`; `115 techniques, 9 problem(s) not audited yet`.
- [ ] **Step 8: Commit** `Stage 6 audit: topic 33 tagged`.

### Task 5: Topic 34, digit DP and speedups

- [ ] **Step 1: Failing tests:**

```python
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
```

- [ ] **Step 2: Run** it: `test_topic_34` fails.
- [ ] **Step 3: Registry:**

```python
    "dp.digit": {
        "name": "Digit DP",
        "explain": "To count numbers up to N with some digit property, build them digit by digit from the left. A "
                   "`tight` flag says the digits so far equal N's: then the next digit can only go up to N's digit, "
                   "otherwise up to 9. Memoise on (position, tight, whatever the property needs).",
    },
    "dp.digit_started": {
        "name": "Leading zeros in digit DP",
        "explain": "Numbers with fewer digits than N appear in digit DP as numbers with leading zeros. Carry a "
                   "`started` flag that turns on at the first non-zero digit, and let leading zeros skip the property "
                   "checks (a leading 0 isn't a digit of the number, nor anyone's neighbour).",
    },
```

- [ ] **Step 4: Tag.**

```bash
python $TAG course/6_specialist_topics/34_digit_dp_and_speedups digit_choices=:dp.digit count_without_digit=recursion.memo,dp.digit:dp.digit_started jump_game_vi=deque.monotonic,dp.recurrence count_digit_one= constrained_subset_sum=greedy.kadane,deque.monotonic,dp.recurrence count_digit_sum_range=recursion.memo,prefix.sums,dp.digit count_stepping_numbers=recursion.memo,prefix.sums,dp.digit,dp.digit_started at_most_n_given_digits=dp.digit number_range=recursion.memo,prefix.sums,dp.digit,dp.digit_started
```

- [ ] **Step 5: Run** the unit tests (all pass) and `--check 34_ coverage`: 9 `ok`; `117 techniques, 0 problem(s) not audited yet`.
- [ ] **Step 6: Commit** `Stage 6 audit: topic 34 tagged: every problem in the course is audited`.

### Task 6: Turn rule 6 strict

**Files:** `technique_coverage.py`, `server.py` (the `--check` coverage line), `tests/test_coverage.py`
(`Rules`), the spec.

- [ ] **Step 1: Failing test.** In `Rules`, replace `test_unaudited_is_a_warning_only` with:

```python
    def test_unaudited_is_an_error(self):
        c = course(("01_a", [("snip", "snippet", "", [], ["t.x", "t.y"]), ("old", "solo", "hard", [], [])]))
        c[1]["old"]["audited"] = False
        errors, warnings = run(c)
        self.assertEqual(errors, ["old (01_a): not audited: give it a USES list"])
        self.assertEqual(warnings, [])
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`: it fails (the line is a warning).
- [ ] **Step 3: Implement.**
  - In `check_coverage`, an unaudited problem appends `f"{name} ({p['topic_id']}): not audited: give it a USES list"`
    to `errors`. `warnings` stays in the return value (always `[]`) so callers don't change.
  - In `server.py`'s `--check`, the coverage line becomes
    `f"  {'FAIL' if errors else 'ok  '} {label:<50} {len(techniques):>2} techniques, every problem audited"`
    when there are no errors, and lists the errors as before when there are.
  - `grep -rn "not audited" web server.py tests` shows nothing else that depends on the old wording.
- [ ] **Step 4: Spec.**
  - Rule 6 becomes: `6. **Every problem is audited.** A problem with neither field is an error. (During Part 2 this was a warning; it turned strict when Stage 6 finished.)`
  - Under "The check", the bullet about warnings becomes: `` `python server.py --check` runs it and fails on any error, an unaudited problem included. ``
  - The "A unit test runs it…" bullet ends: `requires zero errors, which now covers unaudited problems.`
  - In "Part 2", the closing sentence becomes `Rule 6 turned strict when Stage 6 finished: the unit test now requires zero unaudited problems.`
  - The Status line becomes `**Status:** done. Part 1 and all six stages of Part 2 are merged.`
- [ ] **Step 5: Run** the unit tests (all pass) and `python server.py --check coverage`:
  `ok   technique coverage … 117 techniques, every problem audited`; `All good.`
- [ ] **Step 6: Commit** `Technique coverage: an unaudited problem is now an error`.

### Task 7: README, browser check and full verification

- [ ] **Step 1:** README: `414 coding exercises` becomes `415 coding exercises`.
- [ ] **Step 2:** `tests/browser/stage_6.mjs`, with helpers and opening from `stage_5.mjs`. Checks:
  1. `#/t/32_advanced_trees`: the list equals `Jumping with a lifting table | Building a lifting table | Bottom-up without recursion | Lowest common ancestor with lifting | Rerooting`.
  2. Solve `lift_jump` and `tree_ancestor`.
  3. `#/p/subtree_sizes`: `.tech-new h4` is `New technique: Bottom-up without recursion`.
  4. `#/p/sum_of_distances`: `.reveal-box` includes `This uses Bottom-up without recursion` and `Subtree Sizes teaches it`.
  5. Reset progress and placement; solve `bottleneck` and `max_flow`; `#/p/min_cost_flow`: `.tech-banner` includes
     `This uses Bellman-Ford` and `Shortest Paths With Negative Roads`.
  6. No console errors. That is 9 checks.
- [ ] **Step 3:** In `tests/browser/README.md`, add `    bash tests/browser/fresh.sh 8176 stage_6.mjs` after the `stage_5.mjs` line.
- [ ] **Step 4: Run** it: 9 of 9. Then every earlier scenario and Phase 1 (54).
- [ ] **Step 5:** Unit tests all pass. `python server.py --check`: 415 `ok`, `ok   starting check`, `117 techniques,
  every problem audited`, `All good.`
- [ ] **Step 6: Commit** `Technique coverage complete: README count and a browser check for topic 32`.
