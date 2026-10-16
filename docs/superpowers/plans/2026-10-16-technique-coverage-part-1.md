# Technique coverage, Part 1: machinery and the Graph traversal pilot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every problem lists the techniques it uses. Each technique is taught by one basic problem
earlier in the course, and the self-check enforces it. Learners see a "New technique" box, a "Uses"
row, a soft lock that names the problem to do first, a banner for techniques from other topics,
and a "Techniques in this topic" list. Graph traversal is fully audited and fixed.

**Architecture:**
- `course/techniques.py` is a registry of named techniques with explanations.
- Problem files gain `TEACHES` and `USES` lists.
- `server.py` reads them, sorts each topic so teachers come before their users, and serves the
  registry in `/api/course`.
- `technique_coverage.py`, a pure module, checks the rules. It runs in `--check` and in unit tests.
- `web/techniques.js` renders the learner-facing pieces. `app.js` wires them in and extends the
  ladder lock.

**Tech Stack:** Python 3.10+ stdlib server, vanilla JS (no build step), CSS custom properties,
stdlib `unittest`. Browser checks use Node 22's built-in WebSocket with headless Chrome; there are
no npm packages.

**Spec:** `docs/superpowers/specs/2026-10-16-technique-coverage-design.md` (Part 1).

## Global Constraints

- No new dependencies: no pip or npm packages. The desktop build must keep working offline.
- Problem names, topic ids and drill keys never change, so progress, saved code and study plans
  keep working.
- `USES` and `TEACHES` go **after** a problem's function definition (directly above `TESTS =` or
  `STEPS =`). `parse_problem` copies assignments that come before the first `def` into the starter
  code, so tags placed above the function would show up in the learner's editor.
- A teacher is a `snippet`, `guided` or `easy` problem (`parsons` later). Every technique has
  exactly one teacher.
- Locks stay soft: "Open anyway" always works. Study-plan mode and placed-out topics skip locks.
- Use existing colour tokens only. Green means learned or passed.
- Match the surrounding style: dense, few comments, `h(...)` DOM helpers. New view code goes in
  `web/techniques.js`, not `app.js`.
- Tests: `python -m unittest discover -s tests` (one file: add `-p "test_x.py"`). Course
  self-check: `python server.py --check <filter>`.
- End every commit message with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **A broken `course/techniques.py` must not take the course down.** Problems still load, the
   technique UI simply doesn't appear, and `--check` fails loudly. Owners: Task 1 test
   `test_broken_registry_is_skipped_not_fatal`, and Task 2 step "registry error in `--check`".
2. **An unknown technique id in a problem must not break the problem page.** Every UI helper skips
   ids missing from the registry, and the check reports them. Owners: Task 2 test
   `test_unknown_id`, and Task 4 code (`filter((id) => ctx.techniques[id])`).
3. **Problems a learner already solved stay open,** even when a newly added teacher in the same
   topic is unsolved. Owner: Task 4 browser check "solved problems stay open".
4. **Re-ranking `num_islands` from medium to easy keeps study plans and progress working.** Owner:
   Task 3 test `test_every_plan_item_exists`.
5. **A dependency cycle inside a topic must neither hang loading nor pass the check.** Owners: Task 1
   test `test_cycle_does_not_hang`, and Task 2 test `test_cycle_is_an_error`.

---

### Task 1: Registry, problem tags and teaching order (server)

**Files:**
- Modify: `server.py`
  - constants after `PROGRESS_FILE`;
  - Course section, after `load_walkthrough_safely`;
  - `parse_problem` return dict;
  - `CourseCache._build` sort;
  - `/api/course` payload.
- Create: `tests/test_techniques.py`

**Interfaces:**
- Produces:
  - `TECHNIQUES_FILE: Path`.
  - `parse_techniques(path) -> {id: {"name": str, "explain": str}}`. A missing file gives `{}`.
    Anything else wrong raises `ValueError`.
  - `load_techniques_safely(path) -> dict`, which gives `{}` and logs on error.
  - Problem dicts gain:
    - `"uses"`: the raw `USES` value, default `[]`;
    - `"teaches"`: the raw `TEACHES` value, default `[]`;
    - `"audited"`: bool, true when `USES` or `TEACHES` is defined.
  - `ladder_order(found: list[problem]) -> list[problem]`, sorted by
    `(rank, teaching depth, title)`.
  - `techniques_payload(problems, techniques) -> {id: {"name", "explain", "teacher": str | None}}`.
  - `/api/course` gains `"techniques"`, and each problem summary gains `"uses"` and `"teaches"`.

- [ ] **Step 1: Write the failing tests** in `tests/test_techniques.py`:

```python
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402

REGISTRY = '''
TECHNIQUES = {
    "bfs.grid": {"name": "BFS on a grid", "explain": "A queue hands out cells in order of distance."},
    "bfs.multi_source": {"name": "Multi-source BFS", "explain": "Start with every source in the queue."},
}
'''


def write(tmp, source, name="techniques.py"):
    path = Path(tmp) / name
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseTechniques(unittest.TestCase):
    def parse(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            return server.parse_techniques(write(tmp, source))

    def test_parses_names_and_explanations(self):
        t = self.parse(REGISTRY)
        self.assertEqual(list(t), ["bfs.grid", "bfs.multi_source"])
        self.assertEqual(t["bfs.grid"], {"name": "BFS on a grid", "explain": "A queue hands out cells in order of distance."})

    def test_bad_id(self):
        with self.assertRaisesRegex(ValueError, "BFS-Grid"):
            self.parse(REGISTRY.replace('"bfs.grid"', '"BFS-Grid"'))

    def test_missing_explain(self):
        with self.assertRaisesRegex(ValueError, "bfs.grid"):
            self.parse(REGISTRY.replace('"explain": "A queue hands out cells in order of distance."', '"explain": ""'))

    def test_python_errors_become_value_errors(self):
        with self.assertRaisesRegex(ValueError, "techniques.py"):
            self.parse(REGISTRY + "\nTECHNIQUES = {oops\n")

    def test_missing_file_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(server.parse_techniques(Path(tmp) / "techniques.py"), {})

    def test_broken_registry_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(server.load_techniques_safely(write(tmp, "TECHNIQUES = 5\n")), {})


PROBLEM = '''
"""
Spread                                                                        [easy]

Statement.
"""


def spread(grid):
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.multi_source"]
USES = ["bfs.grid"]

TESTS = [((["."],), 0)]
'''


class ProblemTags(unittest.TestCase):
    def test_tags_are_read_and_stay_out_of_the_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = server.parse_problem(write(tmp, PROBLEM, "spread.py"))
        self.assertEqual((p["uses"], p["teaches"], p["audited"]), (["bfs.grid"], ["bfs.multi_source"], True))
        self.assertNotIn("USES", p["starter"])
        self.assertNotIn("TEACHES", p["starter"])

    def test_untagged_problem_is_not_audited(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = server.parse_problem(write(tmp, PROBLEM.replace('TEACHES = ["bfs.multi_source"]\nUSES = ["bfs.grid"]\n', ""), "spread.py"))
        self.assertEqual((p["uses"], p["teaches"], p["audited"]), ([], [], False))


def prob(name, rank, title=None, uses=(), teaches=()):
    return {"name": name, "rank": rank, "title": title or name, "uses": list(uses), "teaches": list(teaches)}


class LadderOrder(unittest.TestCase):
    def test_teacher_comes_first_within_a_rank(self):
        found = [prob("a_user", 2, uses=["t.x"]), prob("z_teacher", 2, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["z_teacher", "a_user"])

    def test_rank_still_comes_first(self):
        found = [prob("hard_one", 4), prob("easy_user", 2, uses=["t.x"]), prob("snip", 0, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["snip", "easy_user", "hard_one"])

    def test_chains_sort_in_teaching_order(self):
        found = [prob("c", 2, uses=["t.y"]), prob("b", 2, uses=["t.x"], teaches=["t.y"]), prob("a", 2, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["a", "b", "c"])

    def test_cycle_does_not_hang(self):
        found = [prob("a", 2, uses=["t.y"], teaches=["t.x"]), prob("b", 2, uses=["t.x"], teaches=["t.y"])]
        self.assertEqual(sorted(p["name"] for p in server.ladder_order(found)), ["a", "b"])

    def test_bad_tag_types_are_ignored_for_ordering(self):
        found = [prob("a", 2), {**prob("b", 2), "uses": "t.x"}]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["a", "b"])


class Payload(unittest.TestCase):
    def test_teacher_names(self):
        techniques = {"t.x": {"name": "X", "explain": "x"}, "t.y": {"name": "Y", "explain": "y"}}
        problems = {"p1": {"teaches": ["t.x"]}, "p2": {"teaches": "nope"}}
        self.assertEqual(server.techniques_payload(problems, techniques),
                         {"t.x": {"name": "X", "explain": "x", "teacher": "p1"},
                          "t.y": {"name": "Y", "explain": "y", "teacher": None}})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_techniques.py"`. Expected:
  errors such as `AttributeError: module 'server' has no attribute 'parse_techniques'`.

- [ ] **Step 3: Constant.** In `server.py`, directly after the `DOORS = (...)` line, add:

```python
TECHNIQUES_FILE = COURSE / "techniques.py"                                # named techniques problems teach and use
```

- [ ] **Step 4: Registry loader, ordering and payload.** In `server.py`, directly after
  `load_walkthrough_safely`, add:

```python
TECHNIQUE_ID = re.compile(r"[a-z0-9_]+\.[a-z0-9_]+")


def parse_techniques(path):
    """course/techniques.py: TECHNIQUES = {"area.variant": {"name", "explain"}}. No file means no techniques."""
    try:
        module = load_module(path)
    except FileNotFoundError:
        return {}
    except Exception as exc:  # noqa: BLE001 - a typo in course content is reported, never fatal
        raise ValueError(f"{path.name}: {type(exc).__name__}: {exc}") from exc
    found = module.get("TECHNIQUES")
    if not isinstance(found, dict):
        raise ValueError(f"{path.name}: TECHNIQUES must be a dict of id -> {{name, explain}}")
    out = {}
    for tid, entry in found.items():
        if not isinstance(tid, str) or not TECHNIQUE_ID.fullmatch(tid):
            raise ValueError(f"{path.name}: bad technique id {tid!r} (use area.variant, lowercase)")
        if not isinstance(entry, dict) or not all(isinstance(entry.get(k), str) and entry[k].strip() for k in ("name", "explain")):
            raise ValueError(f"{path.name}: {tid} needs a name and an explain")
        out[tid] = {"name": entry["name"], "explain": entry["explain"]}
    return out


def load_techniques_safely(path):
    """A broken registry hides the technique UI (and says why) rather than taking the course down."""
    try:
        return parse_techniques(path)
    except ValueError as exc:
        sys.stderr.write(f"  techniques skipped: {exc}\n")
        return {}


def _tag_list(value):
    return value if isinstance(value, list) and all(isinstance(x, str) for x in value) else []


def ladder_order(found):
    """A topic's problems by rank. Within a rank, a problem comes after every same-topic problem that
    teaches a technique it uses (so chains of basics read in teaching order), then by title."""
    teacher = {t: p["name"] for p in found for t in _tag_list(p.get("teaches"))}
    by_name = {p["name"]: p for p in found}
    depth, visiting = {}, set()

    def d(name):
        if name in depth:
            return depth[name]
        if name in visiting:
            return 0                            # a cycle: the coverage check reports it
        visiting.add(name)
        deps = [teacher[t] for t in _tag_list(by_name[name].get("uses")) if teacher.get(t) not in (None, name)]
        depth[name] = 1 + max((d(t) for t in deps), default=-1)
        visiting.discard(name)
        return depth[name]
    return sorted(found, key=lambda p: (p["rank"], d(p["name"]), p["title"].lower()))


def techniques_payload(problems, techniques):
    teacher = {t: name for name, p in problems.items() for t in _tag_list(p.get("teaches"))}
    return {tid: {**info, "teacher": teacher.get(tid)} for tid, info in techniques.items()}
```

- [ ] **Step 5: Problem fields.** In `parse_problem`'s returned dict, after
  `"has_solution": (SOLUTIONS / f"{path.stem}.py").exists(),`, add:

```python
        "uses": module.get("USES", []),
        "teaches": module.get("TEACHES", []),
        "audited": "USES" in module or "TEACHES" in module,
```

- [ ] **Step 6: Teaching order.** In `CourseCache._build`, replace

```python
                found.sort(key=lambda p: (p["rank"], p["title"].lower()))
```

  with

```python
                found = ladder_order(found)
```

- [ ] **Step 7: API.** In `do_GET`'s `/api/course` branch:
  - add `"techniques": techniques_payload(problems, load_techniques_safely(TECHNIQUES_FILE)),` to
    the dict, after `"plans": load_plans(),`;
  - change the problem summary key tuple
    `("name", "title", "kind", "difficulty", "tests", "topic_id")` to
    `("name", "title", "kind", "difficulty", "tests", "topic_id", "uses", "teaches")`.

- [ ] **Step 8: Run** `python -m unittest discover -s tests`. Expected: all pass, including the
  existing tests. Course order is unchanged, because no problem has tags yet.

- [ ] **Step 9: Commit**

```bash
git add server.py tests/test_techniques.py
git commit -m "Techniques: registry, problem tags and teaching order" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: The coverage check

**Files:**
- Create: `technique_coverage.py`. It isn't named `coverage.py`, so it can't be confused with the
  coverage.py package.
- Modify: `server.py` (import, and a block in `check()`)
- Create: `tests/test_coverage.py`

**Interfaces:**
- Consumes:
  - topics as from `load_course()[0]`: dicts with `"id"` and `"items"` in ladder order;
  - problems as from `load_course()[1]`: `"kind"`, `"difficulty"`, `"uses"`, `"teaches"`,
    `"audited"`, `"topic_id"`;
  - techniques from `parse_techniques`.
- Produces: `check_coverage(topics, problems, techniques) -> (errors: list[str], warnings: list[str])`.
  `python server.py --check coverage` runs only this check.

- [ ] **Step 1: Write the failing tests** in `tests/test_coverage.py`:

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  `ModuleNotFoundError: No module named 'technique_coverage'`.

- [ ] **Step 3: Write `technique_coverage.py`**:

```python
"""Technique coverage: every technique a problem uses is taught by exactly one basic problem,
earlier in the course. Pure functions: server.py and the tests feed it the parsed course."""

BASIC_KINDS = {"snippet", "guided", "parsons"}


def is_basic(p):
    return p["kind"] in BASIC_KINDS or p.get("difficulty") == "easy"


def check_coverage(topics, problems, techniques):
    """topics: course order, each {"id", "items"} with items in ladder order. problems: name ->
    {"kind", "difficulty", "uses", "teaches", "audited", "topic_id"}. techniques: id -> {...}.
    Returns (errors, warnings) as plain-English lines."""
    errors, warnings = [], []
    order = {name: i for i, name in enumerate(n for t in topics for n in t["items"])}
    tags, teachers = {"uses": {}, "teaches": {}}, {}
    for name in order:
        p = problems[name]
        if not p["audited"]:
            warnings.append(f"{name} ({p['topic_id']}): not audited yet")
        for field in ("uses", "teaches"):
            ids = p[field]
            if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
                errors.append(f"{name}: {field.upper()} must be a list of technique ids")
                ids = []
            tags[field][name] = ids
            for t in ids:
                if t not in techniques:
                    errors.append(f"{name}: {field.upper()} names {t}, which isn't in course/techniques.py")
        for t in sorted(set(tags["uses"][name]) & set(tags["teaches"][name])):
            errors.append(f"{name}: {t} is in both TEACHES and USES")
        for t in tags["teaches"][name]:
            teachers.setdefault(t, []).append(name)
            if not is_basic(p):
                errors.append(f"{name}: teaches {t}, but a teacher must be a snippet, guided or easy problem "
                              f"(it's {p.get('difficulty') or p['kind']})")
    for t in techniques:
        who = teachers.get(t, [])
        if not who:
            errors.append(f"{t}: no problem teaches it (add it to one basic problem's TEACHES)")
        elif len(who) > 1:
            errors.append(f"{t}: taught by {', '.join(who)}; exactly one problem should teach it")
    for name in order:
        for t in tags["uses"][name]:
            who = teachers.get(t)
            if who and who[0] != name and order[who[0]] > order[name]:
                where = ("later in the same topic" if problems[who[0]]["topic_id"] == problems[name]["topic_id"]
                         else "in a later topic")
                errors.append(f"{name} uses {t}, but its teacher {who[0]} comes {where}")
    return errors, warnings
```

- [ ] **Step 4: Wire it into `--check`.**
  - In `server.py`, after the stdlib imports (after `from urllib.parse import parse_qs, urlparse`),
    add:

```python

from technique_coverage import check_coverage
```

  - In `check()`, directly above `print("\nAll good." if not failures else f"\n{failures} problem(s).")`,
    add:

```python
    if not only or any(o in "coverage" for o in only):
        label = "technique coverage"
        try:
            techniques = parse_techniques(TECHNIQUES_FILE)
        except ValueError as exc:
            failures += 1
            print(f"  FAIL {label:<50} {exc}")
        else:
            errors, warnings = check_coverage(topics, problems, techniques)
            failures += bool(errors)
            print(f"  {'FAIL' if errors else 'ok  '} {label:<50} {len(techniques):>2} techniques, "
                  f"{len(warnings)} problem(s) not audited yet")
            for line in errors:
                print("        ", line)
```

- [ ] **Step 5: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 6: Run** `python server.py --check coverage`. Expected: `ok   technique coverage …
  0 techniques, 383 problem(s) not audited yet` and `All good.`

- [ ] **Step 7: Registry error in `--check`.**
  1. Create a temporary `course/techniques.py` containing `TECHNIQUES = 5`.
  2. Run `python server.py --check coverage`. Expected: a `FAIL technique coverage` line naming
     `techniques.py`, and `1 problem(s).`
  3. Delete the temporary file.

- [ ] **Step 8: Commit**

```bash
git add technique_coverage.py server.py tests/test_coverage.py
git commit -m "Technique coverage check in --check and the tests" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: The Graph traversal pilot (content)

**Files:**
- Create: `course/techniques.py`
- Create: `course/4_advanced/19_graph_traversal/{reachable_nodes,count_enclosed,fewest_steps,key_then_exit,route_to_exit}.py`
- Create: `solutions/{reachable_nodes,count_enclosed,fewest_steps,key_then_exit,route_to_exit}.py`
- Modify: the 14 existing problem files in `course/4_advanced/19_graph_traversal/` (tags;
  `num_islands` re-ranked; `shortest_path_all_keys` hint)
- Modify: `solutions/shortest_path_all_keys.py`
- Modify: `README.md` (exercise count)
- Modify: `tests/test_coverage.py` (pilot tests)

**Interfaces:**
- Consumes: `TEACHES`/`USES` parsing and `ladder_order` (Task 1); `check_coverage` (Task 2).
- Produces: 10 registry techniques, every Graph traversal problem tagged, and 5 new easy problems.
  Task 4's browser checks rely on these names and titles:

| Technique id | Name | Teacher (kind) |
|---|---|---|
| `grid.neighbors` | Grid neighbours | `open_neighbors` (snippet) |
| `bfs.shortest` | BFS for fewest steps | `distance_to_exit` (guided) |
| `bfs.multi_source` | Multi-source BFS | `distance_to_exit` (guided) |
| `dfs.flood_fill` | Flood fill | `flood_fill` (easy) |
| `graph.components` | Counting connected regions | `num_islands` (re-ranked to easy) |
| `graph.adjacency` | Walking a graph from its edges | `reachable_nodes` (new, easy) |
| `flood.from_targets` | Searching back from the targets | `count_enclosed` (new, easy) |
| `bfs.implicit` | BFS with generated neighbours | `fewest_steps` (new, easy) |
| `bfs.state` | BFS over a richer state | `key_then_exit` (new, easy) |
| `bfs.path` | Rebuilding the path | `route_to_exit` (new, easy) |

- [ ] **Step 1: Write the failing pilot tests.** Append to `tests/test_coverage.py`, above the
  `if __name__` line:

```python
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

    def test_every_plan_item_exists(self):
        plans = server.load_plans()["plans"]
        missing = [n for pl in plans for s in pl["sections"] for n in s["items"] if n not in self.problems]
        self.assertEqual(missing, [])
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -p "test_coverage.py"`. Expected:
  failures in `test_every_problem_is_audited` and `test_new_basics_are_easy`, and a `ValueError`
  from `.index()` for the new problem names.

- [ ] **Step 3: The registry.** Create `course/techniques.py`:

```python
"""Every technique a problem may rely on. Each one is taught by exactly one basic problem (the one
that lists it in TEACHES), earlier in the course than any problem that lists it in USES.
`python server.py --check coverage` enforces this. Explanations: 2-4 sentences, inline `code` allowed."""

TECHNIQUES = {
    "grid.neighbors": {
        "name": "Grid neighbours",
        "explain": "A cell (r, c) has up to four neighbours: (r - 1, c), (r + 1, c), (r, c - 1) and (r, c + 1). "
                   "Check `0 <= nr < rows and 0 <= nc < cols` before you look at one, and skip walls.",
    },
    "bfs.shortest": {
        "name": "BFS for fewest steps",
        "explain": "Put the start in a queue at distance 0. Pop a cell and give each unvisited neighbour distance + 1 "
                   "before queueing it. The queue hands out cells in order of distance, so the first time you reach "
                   "a cell is along a shortest path.",
    },
    "bfs.multi_source": {
        "name": "Multi-source BFS",
        "explain": "When there are several starts, put all of them in the queue at distance 0 before the loop. The "
                   "search then spreads from every start at once, and each cell gets its distance to the nearest start.",
    },
    "dfs.flood_fill": {
        "name": "Flood fill",
        "explain": "From one cell, visit every connected cell that matches (same colour, open floor), marking each "
                   "one as you reach it so it's never visited twice. A stack (DFS) or a queue (BFS) both cover the "
                   "whole region.",
    },
    "graph.components": {
        "name": "Counting connected regions",
        "explain": "Scan every cell (or node). Each time you find one you haven't visited, that's a new region: "
                   "count it, then flood fill the whole region so none of its cells starts a region again.",
    },
    "graph.adjacency": {
        "name": "Walking a graph from its edges",
        "explain": "When a graph comes as a list of edges, first build an adjacency list: for an undirected edge "
                   "(a, b), add b to a's list and a to b's. Then BFS or DFS with a `seen` set. The same walk works "
                   "when nodes link to their neighbours directly, like `node.neighbors`.",
    },
    "flood.from_targets": {
        "name": "Searching back from the targets",
        "explain": 'Instead of asking "can this cell reach the edge?" once per cell, search once FROM the targets '
                   "(often the border cells) and mark everything they reach. One flood from many starts replaces "
                   "one search per cell.",
    },
    "bfs.implicit": {
        "name": "BFS with generated neighbours",
        "explain": "Sometimes nobody lists the neighbours: you work them out from the current state, such as a "
                   "number's x + 1, x - 1 and x * 2, or a word with one letter changed. Generate them inside the "
                   "BFS loop and keep a `seen` set of states.",
    },
    "bfs.state": {
        "name": "BFS over a richer state",
        "explain": "When the same cell can matter twice (before and after picking up a key, say), put the extra "
                   "information into the state: (row, col, has_key). The `seen` set holds whole states, so you "
                   "may stand on a cell once per state.",
    },
    "bfs.path": {
        "name": "Rebuilding the path",
        "explain": "BFS finds distances, not routes. Record each cell's parent (the cell you reached it from) the "
                   "first time you see it. When you reach the goal, follow the parents back to the start and reverse.",
    },
}
```

- [ ] **Step 4: The five new problems.** Create each file in
  `course/4_advanced/19_graph_traversal/`.

  `reachable_nodes.py`:

```python
"""
Reachable nodes                                                               [easy]

A graph has nodes 0 to n - 1. `edges` lists undirected edges as pairs (a, b):
you can walk from a to b and from b to a. Return every node you can reach from
`start` (including start itself), sorted.

Example:
    reachable_nodes(5, [(0, 1), (1, 2), (3, 4)], 0)  ->  [0, 1, 2]

Aim for:  O(n + edges).
Hint:     First build the adjacency list: graph = [[] for _ in range(n)], then for each
          edge add b to graph[a] AND a to graph[b]. Then BFS (or DFS) from start with
          a `seen` set, so no node is visited twice.
"""


def reachable_nodes(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["graph.adjacency"]
USES = ["bfs.shortest"]

TESTS = [
    ((5, [(0, 1), (1, 2), (3, 4)], 0), [0, 1, 2]),
    ((5, [(0, 1), (1, 2), (3, 4)], 4), [3, 4]),
    ((3, [], 1), [1]),
    ((4, [(0, 1), (1, 2), (2, 0), (2, 3)], 3), [0, 1, 2, 3]),
    ((6, [(0, 5), (5, 4), (1, 2)], 5), [0, 4, 5]),
]
```

  `count_enclosed.py`:

```python
"""
Count enclosed cells                                                          [easy]

The grid is a list of strings: "." is open, "#" is a wall. Moving up, down,
left or right through open cells, some open cells can reach the edge of the
grid and some are walled in. Return how many open cells can NOT reach the edge.

Example:
    count_enclosed(["#####",
                    "#..##",
                    "#####"])  ->  2

Aim for:  O(rows * cols), with one search, not one search per cell.
Hint:     Search once FROM the edge instead: put every open cell on the border in a stack,
          flood fill from all of them, and mark what you reach. The open cells you never
          reached are the enclosed ones.
"""


def count_enclosed(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["flood.from_targets"]
USES = ["dfs.flood_fill"]

TESTS = [
    ((["#####", "#..##", "#####"],), 2),
    ((["#####", "#.#.#", "#...#", "##.##"],), 0),
    (([".#.", "#.#", ".#."],), 1),
    ((["....", ".##.", ".#..", "...."],), 0),
    ((["######", "#..#.#", "#..#.#", "######"],), 6),
]
```

  `fewest_steps.py`:

```python
"""
Fewest steps to a number                                                      [easy]

Start at the number `start`. Each step changes it by +1, by -1, or doubles it.
Return the fewest steps to reach `target`. The number must stay between 0 and
2 * max(start, target) (going outside that range never helps).

Example:
    fewest_steps(1, 10)  ->  4      (1 -> 2 -> 4 -> 5 -> 10)
    fewest_steps(10, 1)  ->  9

Aim for:  O(max(start, target)).
Hint:     The numbers are the nodes, but nobody gives you a neighbour list: you make it.
          The neighbours of x are x + 1, x - 1 and x * 2 (when they stay in range).
          Then it's the usual BFS from start, with a dict of distances.
"""


def fewest_steps(start: int, target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.implicit"]
USES = ["bfs.shortest"]

TESTS = [
    ((5, 8), 2),
    ((1, 10), 4),
    ((10, 1), 9),
    ((3, 3), 0),
    ((0, 5), 4),
    ((7, 100), 6),
]
```

  `key_then_exit.py`:

```python
"""
Key, door, exit                                                               [easy]

The grid is a list of strings:
    "@"   your start          "E"   the exit
    "."   open floor          "#"   wall
    "k"   a key               "D"   a door: you can walk through it only once you hold the key
Each step moves up, down, left or right. Return the fewest steps to reach the
exit, or -1 if you can't.

Example:
    key_then_exit(["@D.E",
                   "k#.#"])  ->  5
        Down to the key, back up, through the door, then two more steps.

Aim for:  O(rows * cols).
Hint:     A plain BFS on cells breaks: you may need to walk back over a cell after picking up
          the key. So the BFS state is (row, col, has_key), and `seen` holds states, not
          cells. Stepping onto the key sets has_key to True.
"""


def key_then_exit(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.state"]
USES = ["bfs.shortest", "grid.neighbors"]

TESTS = [
    ((["@.E"],), 2),
    ((["@D.E", "k#.#"],), 5),
    ((["@.#E", "k.D."],), 5),
    ((["@#E", "k#."],), -1),
    ((["@...", "##D#", "k..E"],), -1),
    ((["@k", "DE"],), 2),
]
```

  `route_to_exit.py`:

```python
"""
Route to the exit                                                             [easy]

The grid is a list of strings: "S" is the start, "E" the exit, "#" a wall and
"." open floor. Return a shortest route from S to E as a list of (row, col)
cells, both ends included, or [] if there is none.

To make the answer unique: BFS from S, look at neighbours in the order up, down,
left, right, and give each cell its parent the first time you see it.

Example:
    route_to_exit(["S.#",
                   ".#.",
                   "..E"])  ->  [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

Aim for:  O(rows * cols).
Hint:     Keep parent = {start: None}. When BFS first reaches a cell, record the cell it came
          from. When you pop E, follow the parents back to S and reverse the list.
"""


def route_to_exit(grid: list[str]) -> list[tuple[int, int]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.path"]
USES = ["bfs.shortest", "grid.neighbors"]

TESTS = [
    ((["S.E"],), [(0, 0), (0, 1), (0, 2)]),
    ((["S.#", ".#.", "..E"],), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    ((["S#E"],), []),
    ((["S..", "##.", "E.."],), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]),
    ((["S...", ".##.", "...E"],), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3)]),
]
```

- [ ] **Step 5: Their reference solutions.** Create in `solutions/`.

  `reachable_nodes.py`:

```python
from collections import deque


def reachable_nodes(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    graph = [[] for _ in range(n)]
    for a, b in edges:                      # undirected: each edge goes both ways
        graph[a].append(b)
        graph[b].append(a)
    seen, queue = {start}, deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen)
```

  `count_enclosed.py`:

```python
def count_enclosed(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    # Search FROM the edge: every open border cell starts the flood at once.
    stack = [(r, c) for r in range(rows) for c in range(cols)
             if grid[r][c] == "." and (r in (0, rows - 1) or c in (0, cols - 1))]
    safe = set(stack)
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in safe:
                safe.add((nr, nc))
                stack.append((nr, nc))
    return sum(row.count(".") for row in grid) - len(safe)
```

  `fewest_steps.py`:

```python
from collections import deque


def fewest_steps(start: int, target: int) -> int:
    limit = 2 * max(start, target)
    dist, queue = {start: 0}, deque([start])
    while queue:
        x = queue.popleft()
        if x == target:
            return dist[x]
        for nxt in (x + 1, x - 1, x * 2):   # the neighbours are generated, not given
            if 0 <= nxt <= limit and nxt not in dist:
                dist[nxt] = dist[x] + 1
                queue.append(nxt)
    return -1
```

  `key_then_exit.py`:

```python
from collections import deque


def key_then_exit(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    seen, queue = {(*start, False)}, deque([(*start, False, 0)])   # state = (row, col, has_key)
    while queue:
        r, c, has_key, steps = queue.popleft()
        if grid[r][c] == "E":
            return steps
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":
                continue
            if grid[nr][nc] == "D" and not has_key:
                continue                     # locked until we hold the key
            state = (nr, nc, has_key or grid[nr][nc] == "k")
            if state not in seen:
                seen.add(state)
                queue.append((*state, steps + 1))
    return -1
```

  `route_to_exit.py`:

```python
from collections import deque


def route_to_exit(grid: list[str]) -> list[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "S")
    parent, queue = {start: None}, deque([start])
    while queue:
        r, c = queue.popleft()
        if grid[r][c] == "E":
            path, cell = [], (r, c)
            while cell is not None:          # walk the parents back to S
                path.append(cell)
                cell = parent[cell]
            return path[::-1]
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):   # up, down, left, right
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []
```

- [ ] **Step 6: Tag the existing problems.**
  1. Change `num_islands.py`'s header from `[medium] · graphs` to `[easy] · graphs`.
  2. Run this one-off script from the repo root. It inserts each problem's tags directly above its
     `TESTS =` line (or `STEPS =` for the guided problem), and fails if any file lacks one:

```python
import pathlib
TAGS = {
    "open_neighbors": (["grid.neighbors"], []),
    "distance_to_exit": (["bfs.shortest", "bfs.multi_source"], ["grid.neighbors"]),
    "flood_fill": (["dfs.flood_fill"], ["grid.neighbors"]),
    "num_islands": (["graph.components"], ["dfs.flood_fill"]),
    "max_area_island": ([], ["graph.components"]),
    "clone_graph": ([], ["graph.adjacency"]),
    "rotting_oranges": ([], ["bfs.multi_source"]),
    "shortest_path_grid": ([], ["bfs.shortest", "grid.neighbors"]),
    "pacific_atlantic": ([], ["flood.from_targets"]),
    "surrounded_regions": ([], ["flood.from_targets"]),
    "bus_routes": ([], ["graph.adjacency", "bfs.shortest"]),
    "shortest_path_all_keys": ([], ["bfs.state"]),
    "word_ladder": ([], ["bfs.implicit"]),
    "solve_maze": ([], ["bfs.path"]),
}
base = pathlib.Path("course/4_advanced/19_graph_traversal")
for name, (teaches, uses) in TAGS.items():
    path = base / f"{name}.py"
    lines = path.read_text(encoding="utf-8").split("\n")
    at = next(i for i, line in enumerate(lines) if line.startswith(("TESTS =", "STEPS =")))
    block = ([f"TEACHES = {teaches!r}".replace("'", '"')] if teaches else []) + [f"USES = {uses!r}".replace("'", '"'), ""]
    path.write_text("\n".join(lines[:at] + block + lines[at:]), encoding="utf-8")
    print("tagged", name)
```

- [ ] **Step 7: `shortest_path_all_keys` without bitmasks.** It no longer needs Bit tricks
  (topic 25).
  - In `course/4_advanced/19_graph_traversal/shortest_path_all_keys.py`, replace the four `Hint:`
    lines

```
Hint:     A plain BFS on cells fails, because you may need to come back to a cell after picking
          up a key. So make the state (r, c, mask) where bit i of mask = holding key i. Picking up
          a key sets its bit. A lock is passable when its bit is set. Stop when mask has every
          key's bit.
```

    with

```
Hint:     A plain BFS on cells fails, because you may need to come back to a cell after picking
          up a key. So make the state (r, c, keys), where keys is a frozenset of the keys you
          hold. Picking up a key adds it. A lock is passable when its lowercase letter is in
          keys. Stop when you hold every key. (A bitmask works too, if you know bit tricks.)
```

  - Replace all of `solutions/shortest_path_all_keys.py` with:

```python
from collections import deque


def shortest_path_all_keys(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    total = sum(ch.islower() for row in grid for ch in row)
    first = (*start, frozenset())
    seen, queue = {first}, deque([(first, 0)])      # state = (row, col, keys held)
    while queue:
        (r, c, keys), steps = queue.popleft()
        if len(keys) == total:
            return steps
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":
                continue
            ch = grid[nr][nc]
            if ch.isupper() and ch.lower() not in keys:
                continue                              # locked, and we don't have its key yet
            state = (nr, nc, (keys | {ch}) if ch.islower() else keys)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))
    return -1
```

- [ ] **Step 8: README.** Replace `34 topics in 6 stages, 383 coding exercises` with
  `34 topics in 6 stages, 388 coding exercises`.

- [ ] **Step 9: Run** `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 10: Run** `python server.py --check 19_graph coverage`. Expected:
  - every Graph traversal line `ok` (19 problems, including the 5 new ones);
  - `ok   technique coverage … 10 techniques, 369 problem(s) not audited yet`;
  - `All good.`

  If a new problem's reference solution fails, the solution is wrong, not the test: the expected
  values were computed by running these exact solutions.

- [ ] **Step 11: Commit**

```bash
git add course/techniques.py course/4_advanced/19_graph_traversal solutions README.md tests/test_coverage.py
git commit -m "Graph traversal: techniques registry, tags and five new basic problems" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: What the learner sees, plus browser checks

**Files:**
- Create: `web/techniques.js`
- Modify: `web/index.html` (load it before `app.js`)
- Modify: `web/app.js`
  - boot;
  - technique helpers after `T.reachedTopics`;
  - `blocker`;
  - the lock message;
  - the problem tab;
  - the topic page.
- Modify: `web/app.css`
- Create: `tests/browser/cdp.mjs`, `tests/browser/fresh.sh`, `tests/browser/technique_coverage.mjs`,
  `tests/browser/README.md`

**Interfaces:**
- Consumes: `/api/course` `"techniques"` and problem `"uses"`/`"teaches"` (Task 1); the pilot
  content (Task 3); `placedOut`, `solved`, `topicOf`, `topicTitle` (existing in `app.js`).
- Produces:
  - `T.techniqueBoxes(problem, ctx) -> Element[]`
  - `T.usesRow(problem, ctx) -> Element | null`
  - `T.techniqueBanner(problem, topic, ctx) -> Element | null`
  - `T.topicTechniques(topic, ctx) -> Element[] | null`

  `ctx` is
  `{techniques, known(id), teacherHref(id), teacherTitle(id), teacherTopic(id), topicTitle(topic), taughtIn(topic)}`.

- [ ] **Step 1: Write `web/techniques.js`**:

```js
"use strict";
/* Techniques: the "New technique" box on teaching problems, the "Uses" row on every problem, the
   banner for techniques taught in other topics, and a topic's list of techniques. */
(function () {
  const T = window.Trace;
  const { h } = T;

  // ctx comes from app.js: techniques, known(id), teacherHref(id), teacherTitle(id), teacherTopic(id),
  // topicTitle(topic), taughtIn(topic). Ids missing from the registry are skipped everywhere.
  T.techniqueBoxes = (problem, ctx) => (problem.teaches || []).filter((id) => ctx.techniques[id]).map((id) =>
    h("section", { class: "tech-new", "aria-label": "New technique" },
      h("h4", {}, "New technique: ", ctx.techniques[id].name),
      h("p", {}, T.inline(ctx.techniques[id].explain))));

  T.usesRow = (problem, ctx) => {
    const ids = (problem.uses || []).filter((id) => ctx.techniques[id]);
    if (!ids.length) return null;
    const detail = h("div", { class: "tech-detail", hidden: true });
    let open = null;
    const chips = ids.map((id) => h("button", {
      type: "button", class: "tech-chip" + (ctx.known(id) ? " known" : ""), "aria-expanded": "false",
      onclick: (e) => {
        open = open === id ? null : id;
        chips.forEach((b) => b.setAttribute("aria-expanded", String(b === e.currentTarget && open === id)));
        detail.hidden = !open;
        if (open) detail.replaceChildren(h("p", {}, T.inline(ctx.techniques[id].explain)),
          ctx.teacherHref(id) ? h("p", { class: "tech-teacher" }, ctx.known(id) ? "Learned in " : "Taught in ",
            h("a", { class: "link", href: ctx.teacherHref(id) }, ctx.teacherTitle(id))) : null);
      },
    }, ctx.known(id) ? "✓ " : "", ctx.techniques[id].name));
    return h("div", { class: "tech-uses-wrap" }, h("div", { class: "tech-uses" }, h("span", { class: "tech-label" }, "Uses"), chips), detail);
  };

  T.techniqueBanner = (problem, topic, ctx) => {
    const missing = (problem.uses || []).filter((id) => ctx.techniques[id] && !ctx.known(id)
      && ctx.teacherTopic(id) && ctx.teacherTopic(id).id !== topic.id);
    if (!missing.length) return null;
    return h("div", { class: "tech-banner" }, missing.map((id) => h("p", {}, "This uses ", h("strong", {}, ctx.techniques[id].name),
      ` (${ctx.topicTitle(ctx.teacherTopic(id))}). If it's new to you, try `,
      h("a", { class: "link", href: ctx.teacherHref(id) }, ctx.teacherTitle(id)), " first.")));
  };

  T.topicTechniques = (topic, ctx) => {
    const ids = ctx.taughtIn(topic);
    if (!ids.length) return null;
    return [h("h2", { class: "section-title" }, "Techniques in this topic"),
      h("div", { class: "items tech-list" }, ids.map((id) => h("a", { class: "item" + (ctx.known(id) ? " solved" : ""), href: ctx.teacherHref(id) },
        h("span", { class: "state" }), h("span", { class: "t" }, ctx.techniques[id].name),
        h("span", { class: "meta" }, ctx.teacherTitle(id)), h("span"))))];
  };
})();
```

- [ ] **Step 2: Load it.** In `web/index.html`, after `<script src="start.js"></script>`, add
  `<script src="techniques.js"></script>`.

- [ ] **Step 3: Boot.** In `app.js`'s `boot()`, after `S.plans = data.plans || S.plans;`, add:

```js
      S.techniques = data.techniques || {};
```

- [ ] **Step 4: Helpers.** In `app.js`, directly after the `T.reachedTopics = () => { … };` block,
  add:

```js
  // A technique is known once its teacher is solved, or its teacher's topic is placed out.
  const techTeacher = (id) => (S.techniques || {})[id]?.teacher || null;
  const techKnown = (id) => { const t = techTeacher(id); return !!t && (solved(t) || placedOut(topicOf(t))); };
  const techCtx = () => ({
    techniques: S.techniques || {}, known: techKnown,
    teacherHref: (id) => (techTeacher(id) ? `#/p/${techTeacher(id)}` : null),
    teacherTitle: (id) => (techTeacher(id) ? S.problems[techTeacher(id)].title : ""),
    teacherTopic: (id) => (techTeacher(id) ? topicOf(techTeacher(id)) : null),
    topicTitle,
    taughtIn: (topic) => topic.items.flatMap((n) => S.problems[n].teaches || []).filter((id) => (S.techniques || {})[id]),
  });
```

- [ ] **Step 5: The lock.** In `blocker()`:
  - replace the comment line
    `  // Ladder rule: snippet → guided → all solo problems open together → build after two solos.`
    with
    `  // Ladder rule: snippet → guided → solos together → build after two solos, and never before a same-topic teacher of a technique it uses.`
  - replace its final

```js
    return null;
  }
  function isUnlocked(topic, name) {
```

    with

```js
    return (S.problems[name].uses || []).map(techTeacher).find((t) => t && t !== name && topic.items.includes(t) && !solved(t)) || null;
  }
  function isUnlocked(topic, name) {
```

- [ ] **Step 6: The lock message.** In `renderLeft()`, replace

```js
            S.problems[name].kind === "build" && S.problems[before].kind === "solo"
              ? h("p", {}, "The build opens once you've solved two of this topic's problems. It combines what they teach.")
```

  with

```js
            (S.problems[name].uses || []).some((t) => techTeacher(t) === before)
              ? h("p", {}, "This uses ", h("strong", {}, S.techniques[(S.problems[name].uses || []).find((t) => techTeacher(t) === before)].name),
                ". ", h("strong", {}, S.problems[before].title), " teaches it, so do that one first.")
              : S.problems[name].kind === "build" && S.problems[before].kind === "solo"
              ? h("p", {}, "The build opens once you've solved two of this topic's problems. It combines what they teach.")
```

- [ ] **Step 7: The problem tab.** In `renderLeft()`, replace

```js
          showHowTo
            ? T.howToCard({ onClose: () => { showHowTo = false; local.set("trace.howtoSeen", true); renderLeft(); } })
            : h("button", { class: "link howto-link", type: "button", onclick: () => { showHowTo = true; renderLeft(); } }, "How to work a problem"),
          h("div", { class: "body-text" }, renderStatement(p.statement)));
```

  with

```js
          T.usesRow(S.problems[name], techCtx()),
          T.techniqueBanner(S.problems[name], topic, techCtx()),
          showHowTo
            ? T.howToCard({ onClose: () => { showHowTo = false; local.set("trace.howtoSeen", true); renderLeft(); } })
            : h("button", { class: "link howto-link", type: "button", onclick: () => { showHowTo = true; renderLeft(); } }, "How to work a problem"),
          T.techniqueBoxes(S.problems[name], techCtx()),
          h("div", { class: "body-text" }, renderStatement(p.statement)));
```

- [ ] **Step 8: The topic page.** In `viewTopic()`, replace `      topic.has_lesson ? sheet : null));`
  with:

```js
      T.topicTechniques(topic, techCtx()),
      topic.has_lesson ? sheet : null));
```

- [ ] **Step 9: Styles.** Append to `web/app.css`:

```css
/* ── Techniques ──────────────────────────────────────── */
.tech-uses { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 12px; }
.tech-label { font-size: 12.5px; font-weight: 600; color: var(--ink-3); margin-right: 2px; }
.tech-chip { border: 0; border-radius: 999px; padding: 3px 10px; font-size: 12.5px; font-weight: 500; background: var(--fill-2); color: var(--ink-2); cursor: pointer; }
.tech-chip.known { color: var(--ok); background: var(--ok-soft); }
.tech-chip[aria-expanded="true"] { box-shadow: inset 0 0 0 1.5px var(--accent); }
.tech-detail { margin-top: 8px; padding: 10px 14px; border-radius: var(--radius); background: var(--fill); color: var(--ink-2); font-size: 14.5px; }
.tech-detail p { margin: 0; }
.tech-detail p + p { margin-top: 6px; }
.tech-new { margin: 16px 0 0; padding: 14px 16px; border-radius: var(--radius); background: var(--accent-soft); }
.tech-new h4 { margin: 0 0 4px; font-size: 13px; font-weight: 600; color: var(--accent); }
.tech-new p { margin: 0; color: var(--ink-2); }
.tech-banner { margin-top: 12px; padding: 10px 14px; border-radius: var(--radius); background: var(--fill); color: var(--ink-2); font-size: 14.5px; }
.tech-banner p { margin: 0; }
.tech-banner p + p { margin-top: 6px; }
```

- [ ] **Step 10: Syntax check** with `node --check web/techniques.js && node --check web/app.js`.

- [ ] **Step 11: Browser tooling.** Commit the headless driver used in Phase 1, so later phases can
  reuse it.
  - `tests/browser/cdp.mjs`:

```js
// Minimal headless-Chrome driver over the DevTools protocol (Node 22+ has a global WebSocket).
// Each open() gets a fresh profile, so localStorage starts empty. Set CHROME to override the path.
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function open(url, { width = 1280, height = 900, dark = false } = {}) {
  const dir = mkdtempSync(join(tmpdir(), "trace-cdp-"));
  const port = 9300 + Math.floor(Math.random() * 600);
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${dir}`,
    `--window-size=${width},${height}`, "--no-first-run", "--no-default-browser-check", "about:blank"], { stdio: "ignore" });
  let ws;
  for (let i = 0; i < 60 && !ws; i++) {
    try {
      const page = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page");
      if (page) ws = new WebSocket(page.webSocketDebuggerUrl);
    } catch { /* not up yet */ }
    if (!ws) await sleep(250);
  }
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  let id = 0;
  const pending = new Map(), logs = [];
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
    else if (m.method === "Runtime.exceptionThrown") logs.push("EXCEPTION " + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
    else if (m.method === "Runtime.consoleAPICalled" && ["error", "warning"].includes(m.params.type))
      logs.push(m.params.type + " " + m.params.args.map((a) => a.value ?? a.description).join(" "));
  });
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  await send("Runtime.enable");
  await send("Page.enable");
  if (dark) await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "dark" }] });
  const page = {
    logs,
    async go(u, wait = 1500) { await send("Page.navigate", { url: u }); await sleep(wait); },
    async reload(u) { await page.go("about:blank", 300); await page.go(u); },
    async eval(expr) {
      const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
      if (r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text);
      return r.result.result.value;
    },
    async key(key, code = key) {
      for (const type of ["keyDown", "keyUp"]) await send("Input.dispatchKeyEvent", { type, key, code, text: type === "keyDown" ? (key === "Enter" ? "\r" : key.length === 1 ? key : undefined) : undefined, windowsVirtualKeyCode: key === "Enter" ? 13 : key.charCodeAt(0) });
      await sleep(150);
    },
    async shot(path) { const r = await send("Page.captureScreenshot", { format: "png" }); writeFileSync(path, Buffer.from(r.result.data, "base64")); },
    async close() { ws.close(); proc.kill(); },
  };
  await page.go(url);
  return page;
}

export const results = [];
export function check(name, ok, detail = "") {
  results.push(ok);
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  — " + detail : ""}`);
}
export function summary() {
  const failed = results.filter((r) => !r).length;
  console.log(`\n${results.length - failed}/${results.length} checks passed`);
  process.exitCode = failed ? 1 : 0;
}
```

  - `tests/browser/fresh.sh`:

```bash
#!/usr/bin/env bash
# fresh.sh PORT SCENARIO.mjs: start Trace on an empty workspace, run a scenario against it, stop it.
PORT=$1; shift
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
WS="$(python -c 'import tempfile; print(tempfile.mkdtemp())')"
cd "$ROOT"
TRACE_WORKSPACE="$WS" python server.py --no-browser --port "$PORT" > "$WS/server.log" 2>&1 &
SERVER=$!
for i in $(seq 1 120); do curl -s "localhost:$PORT/api/docker" > /dev/null && break; sleep 1; done
cd "$HERE"
node "$@" "http://localhost:$PORT"
CODE=$?
kill $SERVER 2>/dev/null
exit $CODE
```

  - `tests/browser/README.md`:

```markdown
# Browser checks

Headless-Chrome scenarios for the screens the unit tests can't reach. They need Node 22+ (for its
built-in WebSocket) and Chrome; set `CHROME` if it isn't at the default Windows path. Each run
starts Trace on an empty workspace with a fresh browser profile:

    bash tests/browser/fresh.sh 8170 technique_coverage.mjs

These aren't part of `python -m unittest`; run them when you change a screen.
```

  - `tests/browser/technique_coverage.mjs`:

```js
// Technique coverage: the box, the Uses row, the in-topic lock, plan mode, placement, the topic list.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const text = (p, sel) => p.eval(`document.querySelector(${JSON.stringify(sel)})?.textContent || ""`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// A teaching problem shows its "New technique" box and no Uses row.
await p.reload(BASE + "/#/p/open_neighbors");
check("teaching problem shows the New technique box", (await text(p, ".tech-new h4")) === "New technique: Grid neighbours");
check("a problem with no USES has no Uses row", !(await p.eval(`!!document.querySelector(".tech-uses")`)));

// Solve the snippet and the guided problem, then hit the technique lock.
check("solve open_neighbors", await solve(p, "open_neighbors"));
check("solve distance_to_exit", await solve(p, "distance_to_exit"));
await p.reload(BASE + "/#/p/count_enclosed");
const lock = await text(p, ".reveal-box");
check("in-topic lock names the technique and its teacher", lock.includes("This uses Flood fill") && lock.includes("Flood Fill teaches it"), lock);
check("lock offers Open anyway", (await p.eval(`[...document.querySelectorAll(".reveal-box button")].some(b => b.textContent === "Open anyway")`)));

// Solved problems stay open even with an unsolved same-topic teacher.
check("solve max_area_island directly", await solve(p, "max_area_island"));
await p.reload(BASE + "/#/p/max_area_island");
check("solved problems stay open", !(await p.eval(`!!document.querySelector(".reveal-box button")`)) && (await text(p, ".statement h1")) === "Max Area of Island");

// Solving the teacher opens the problem; the chip is known and explains itself.
check("solve flood_fill", await solve(p, "flood_fill"));
await p.reload(BASE + "/#/p/count_enclosed");
check("problem opens once its teacher is solved", (await text(p, ".statement h1")) === "Count enclosed cells");
check("Uses chip shows as known", (await text(p, ".tech-chip.known")).includes("Flood fill"));
check("teaching box for the new technique", (await text(p, ".tech-new h4")) === "New technique: Searching back from the targets");
await p.eval(`document.querySelector(".tech-chip").click()`); await sleep(200);
check("chip opens its explanation and teacher link", (await text(p, ".tech-detail")).includes("Learned in Flood Fill"));

// Plan mode: no lock, chips still show what's missing.
const planned = await p.eval(`fetch("/api/course").then(r => r.json()).then(d => { for (const pl of d.plans.plans) for (const s of pl.sections) if (s.items.includes("clone_graph")) return pl.id; return null; })`);
if (planned) {
  await p.reload(BASE + `/#/p/clone_graph/plan/${planned}`);
  check("plan mode skips the technique lock", (await text(p, ".statement h1")) === "Clone Graph");
  check("plan mode chip shows the unlearned technique", (await text(p, ".tech-chip:not(.known)")).includes("Walking a graph from its edges"));
}

// The topic page lists the techniques in teaching order, with ticks for learned ones.
await p.reload(BASE + "/#/t/19_graph_traversal");
const list = await p.eval(`[...document.querySelectorAll(".tech-list .item")].map(a => (a.classList.contains("solved") ? "✓" : "") + a.querySelector(".t").textContent)`);
check("topic lists 10 techniques", list.length === 10, list.join(" | "));
check("learned techniques are ticked", list[0] === "✓Grid neighbours" && list.includes("✓Flood fill") && list.includes("Rebuilding the path"), list.join(" | "));

// The banner, through the helper with a technique taught in another topic.
const banner = await p.eval(`(() => { const el = Trace.techniqueBanner({ uses: ["x.y"] }, { id: "19_graph_traversal" }, {
  techniques: { "x.y": { name: "Sliding window", explain: "e" } }, known: () => false,
  teacherHref: () => "#/p/max_sum_subarray_k", teacherTitle: () => "Maximum Sum of k in a Row",
  teacherTopic: () => ({ id: "07_sliding_window" }), topicTitle: () => "Sliding window" }); return el ? el.textContent : ""; })()`);
check("banner names the technique, its topic and its teacher", banner.includes("This uses Sliding window (Sliding window)") && banner.includes("Maximum Sum of k in a Row"), banner);

// Placed-out topics have no technique locks.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "dsa", ready: {}, answers: { "19_graph_traversal": [true] } });
await p.reload(BASE + "/#/p/count_enclosed");
check("placed-out topic: no technique lock", (await text(p, ".statement h1")) === "Count enclosed cells");

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.shot("technique_coverage.png");
await p.close();
summary();
```

- [ ] **Step 12: Run the browser checks** with
  `bash tests/browser/fresh.sh 8170 technique_coverage.mjs`. Expected: every line `PASS`, ending
  with `N/N checks passed`.

  Then open `tests/browser/technique_coverage.png` and check the page looks right in dark mode.
  Delete the screenshot; it isn't committed.

- [ ] **Step 13: Commit**

```bash
git add web/techniques.js web/index.html web/app.js web/app.css tests/browser/cdp.mjs tests/browser/fresh.sh tests/browser/technique_coverage.mjs tests/browser/README.md
git commit -m "Technique coverage on screen: New technique box, Uses row, lock, banner, topic list" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Full verification

**Files:** none new; fixes only if a check fails.

- [ ] **Step 1: Unit tests.** Run `python -m unittest discover -s tests`. Expected: all pass.

- [ ] **Step 2: The whole course.** Run `python server.py --check`. Expected:
  - every problem `ok`;
  - `ok   starting check`;
  - `ok   technique coverage … 10 techniques, 369 problem(s) not audited yet`;
  - `All good.`

  This takes a few minutes.

- [ ] **Step 3: Syntax.** Run
  `node --check web/techniques.js && node --check web/app.js && node --check tests/browser/cdp.mjs && node --check tests/browser/technique_coverage.mjs`.

- [ ] **Step 4: Phase 1 still works.** Re-run the Phase 1 browser scenarios against the new
  screens. They live in this session's scratchpad (`scratchpad/cdp/t4.mjs` … `t8.mjs`); run each
  with `bash fresh.sh <port> tN.mjs` from that folder. Expected: all checks pass, 54 in total.

  If the scratchpad is gone, check by hand instead:
  - the first visit opens "Where are you starting?";
  - the Today card appears;
  - "Placed out" tags appear;
  - the how-to card appears.

- [ ] **Step 5: Commit any fixes** with a message naming what was fixed. If nothing changed, there's
  nothing to commit.
