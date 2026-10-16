# Starting check and first hour Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A first-time learner answers "Where are you starting?", takes a short adaptive check, and lands on their first gap. Big-O comes before the toolkit, home leads with a "Today" card, the first problem shows a "How to work a problem" card, and *Spot the pattern* only mixes topics the learner has reached.

**Architecture:**
- **Server (`server.py`):**
  - `parse_starting_check()` validates the new content file `course/starting_check.py`.
  - `place()`, a pure function, turns answers into `{start, placed_out}`.
  - `record_placement()` validates a finished check and stores it in `progress.json`.
  - Two routes: `GET /api/starting-check` and `POST /api/placement`.
- **Frontend:**
  - New view module `web/start.js`: the doors, the adaptive check, the result screen, and the how-to card.
  - Small hooks in `web/app.js`: route, first-visit redirect, placed-out topics, the Today card, `T.reachedTopics()`.
  - `web/topics/review.js` filters *Spot the pattern* to reached topics.
- **Content:** the topic folder swap and the 56 check questions.

**Tech Stack:** Python 3.10+ stdlib server, vanilla JS (no build step), CSS custom properties, stdlib `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-16-beginner-path-design.md`, section "Phase 1: Starting check and first hour".

## Global Constraints

- No new dependencies: no pip or npm packages, no new fonts. The desktop build must keep working offline.
- Calm design: no streaks, badges or reminders. Use only existing colour tokens (`--accent`, `--fill`, `--ok`, `--bad`, …), so dark mode needs no new values.
- Green only for correct/passed, orange-red only for wrong/failed.
- Topic ids are folder names (`04_hashing`). Problem names, walkthrough topic ids and drill keys (`python-costs/cost`) must not change, so existing progress survives.
- New view logic lives in `web/start.js`, not `app.js`. Match the surrounding style: dense, few comments, `h(...)` DOM helpers.
- Tests: `python -m unittest discover -s tests -v`. Course self-check: `python server.py --check <filter>`.
- End every commit message with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Existing learners are never redirected.** Someone with progress but no placement must never be sent to `#/start`; they see "Take the starting check" in the Today card. Owner: Task 4, step "Manual: existing learner".
2. **A broken or missing `course/starting_check.py` doesn't break Trace.** `/api/starting-check` answers 404 or 500 with the reason, the start screen says the check isn't available and links to the topics, and home still works. Owners: Task 2 test `test_missing_file`, and Task 4, step "Manual: missing file".
3. **Bad placement posts are rejected.** An unknown door, unknown topic, non-boolean answers or more than two answers per topic are rejected, and progress is left untouched. Owner: Task 2 test `test_rejects_bad_input_without_touching_progress`.
4. **A retake replaces the old result completely,** with no stale placed-out topics. Owner: Task 2 test `test_retake_replaces_the_old_result`.
5. **Spot the pattern before it opens.** Opened by URL or Ctrl+K before four pattern topics are reached, it shows the explanation, not an empty drill, and records no run. Owner: Task 7, step "Manual: Spot the pattern gate".

---

### Task 1: Big-O before the toolkit

**Files:**
- Rename: `course/1_foundations/01_python_toolkit/` → `course/1_foundations/02_python_toolkit/`
- Rename: `course/1_foundations/02_big_o_in_practice/` → `course/1_foundations/01_big_o_in_practice/`
- Modify: `web/topics/foundations.js` (the `n` of two drill topics)
- Modify: `course/1_foundations/01_big_o_in_practice/count_bad_pairs.py`, `top_visitors.py` (hints)
- Modify: `server.py` (`CourseCache._build`: add `stage_n`)
- Create: `tests/test_course_order.py`

**Interfaces:**
- Produces: every topic dict from `server.load_course()[0]` (and in `/api/course`) gains `"stage_n": int`, the number prefix of its stage folder (1–6). Tasks 2 and 4 use it.

- [ ] **Step 1: Write the failing tests** in `tests/test_course_order.py`:

```python
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class CourseOrder(unittest.TestCase):
    def setUp(self):
        self.topics, self.problems = server.load_course()

    def test_big_o_comes_before_the_toolkit(self):
        self.assertEqual([t["id"] for t in self.topics[:2]], ["01_big_o_in_practice", "02_python_toolkit"])

    def test_problem_names_survive_the_swap(self):
        by_id = {t["id"]: t for t in self.topics}
        self.assertIn("missing_number", by_id["01_big_o_in_practice"]["items"])
        self.assertIn("running_sum", by_id["02_python_toolkit"]["items"])

    def test_topics_know_their_stage_number(self):
        self.assertEqual({t["stage_n"] for t in self.topics}, {1, 2, 3, 4, 5, 6})
        self.assertEqual(next(t for t in self.topics if t["id"] == "12_stacks")["stage_n"], 3)

    def test_big_o_hints_do_not_assume_the_toolkit(self):
        for name, p in self.problems.items():
            if p["topic_id"] == "01_big_o_in_practice":
                self.assertNotIn("Counter", p["hint"], name)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run** `python -m unittest tests.test_course_order -v`. Expected: 4 failures (topic order, a `KeyError` on `stage_n`, and `Counter` found in a hint).

- [ ] **Step 3: Swap the folders**

```bash
git mv course/1_foundations/01_python_toolkit course/1_foundations/02_python_toolkit
git mv course/1_foundations/02_big_o_in_practice course/1_foundations/01_big_o_in_practice
```

- [ ] **Step 4: Swap the drill topics' numbers** in `web/topics/foundations.js`:
  - `id: "python-costs", n: 1, stage: STAGE,` becomes `id: "python-costs", n: 2, stage: STAGE,`
  - `id: "big-o", n: 2, stage: STAGE,` becomes `id: "big-o", n: 1, stage: STAGE,`

  `app.js` pairs drill topics with course topics by `n`, so this keeps each topic's drills attached to it.

- [ ] **Step 5: Reword the two hints.**
  - In `course/1_foundations/01_big_o_in_practice/count_bad_pairs.py`, replace
    `          So count the GOOD pairs instead: group indices by nums[k] - k with a Counter.`
    with
    `          So count the GOOD pairs instead: count how many indices share each nums[k] - k, in a dict.`
  - In `course/1_foundations/01_big_o_in_practice/top_visitors.py`, replace
    `Hint:     Count with a dict (or Counter), then sort the distinct IPs by (-count, ip)`
    with
    `Hint:     Count with a dict, then sort the distinct IPs by (-count, ip)`

- [ ] **Step 6: Add `stage_n`.** In `server.py`, `CourseCache._build`, add one line to the topic dict, after `"stage": folder_label(stage_dir.name),`:

```python
                    "stage_n": int(re.match(r"^(\d+)", stage_dir.name).group(1)),
```

- [ ] **Step 7: Run** `python -m unittest discover -s tests -v`. Expected: all pass, including the existing walkthrough tests.

- [ ] **Step 8: Check the swapped topics still work** with `python server.py --check 01_big 02_python`. Expected: every line `ok`, ending with `All good.`

- [ ] **Step 9: Commit**

```bash
git add -A course/1_foundations web/topics/foundations.js server.py tests/test_course_order.py
git commit -m "Teach Big-O before the Python toolkit" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Starting check parsing, placement and API (server)

**Files:**
- Modify: `server.py`
  - constants after `PROGRESS_FILE`;
  - Course section, after `load_walkthrough_safely`;
  - progress functions, after `record_walkthrough`;
  - `load_progress`;
  - `do_GET` and `do_POST`.
- Create: `tests/test_starting_check.py`

**Interfaces:**
- Consumes: `stage_n` on topics (Task 1); `load_module`, `load_course`, `update_progress`, `load_progress` (existing).
- Produces:
  - `STARTING_CHECK: Path`, `SKILLS: tuple[str, ...]`, `DOORS: tuple[str, ...]`.
  - `parse_starting_check(path, topics) -> {"ready": [question + {"skill"}], "topics": [{"id", "title", "stage_n", "questions": [q1, q2]}]}`. Only Stage 1–4 topics are included, in course order. A question is `{"question", "options", "answer", "explain", "code", "output"}`, where `code` is dedented (`""` if none) and `output` is a bool. It raises `ValueError`, or `FileNotFoundError` when the file is missing.
  - `place(door, ready, answers, topic_order) -> {"start": str | None, "placed_out": [str]}`.
  - `record_placement(door, ready=None, answers=None) -> progress dict`. It raises `ValueError` on bad input.
  - `reset_progress() -> progress dict`.
  - `GET /api/starting-check` returns the parsed payload, 404 if the file is missing, 500 with the message if it's invalid.
  - `POST /api/placement {"door", "ready", "answers"}` returns `{"progress"}`, or 400 with the message.
  - `progress["placement"]` is `None` (not taken), `{"door", "date"}` for doors new and skip, or `{"door", "date", "ready", "placed_out", "start"}`.

- [ ] **Step 1: Write the failing tests** in `tests/test_starting_check.py`:

```python
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402

TOPICS = [{"id": "01_a", "title": "A", "stage_n": 1}, {"id": "06_b", "title": "B", "stage_n": 2},
          {"id": "30_z", "title": "Z", "stage_n": 6}]

GOOD = '''
SKILLS = ("names", "loops", "functions", "lists", "dicts", "objects")
READY = [{"skill": s, "question": "What does this print?", "code": "print(1)", "options": ["1", "2"],
          "answer": 0, "explain": "e", "output": True} for s in SKILLS]
Q = {"question": "q", "options": ["x", "y"], "answer": 1, "explain": "e"}
TOPICS = {"01_a": [Q, dict(Q, code="""
    a = 1
    print(a)
""")], "06_b": [Q, Q]}
'''


def write(tmp, source):
    path = Path(tmp) / "starting_check.py"
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseStartingCheck(unittest.TestCase):
    def parse(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            return server.parse_starting_check(write(tmp, source), TOPICS)

    def test_parses_stage_1_to_4_in_course_order(self):
        check = self.parse(GOOD)
        self.assertEqual([t["id"] for t in check["topics"]], ["01_a", "06_b"])
        self.assertEqual(check["topics"][0]["questions"][1]["code"], "a = 1\nprint(a)")
        self.assertEqual(check["topics"][0]["questions"][0]["code"], "")
        self.assertEqual([q["skill"] for q in check["ready"]], list(server.SKILLS))
        self.assertTrue(check["ready"][0]["output"])
        self.assertFalse(check["topics"][1]["questions"][0]["output"])

    def test_bad_answer_index_names_the_question(self):
        with self.assertRaisesRegex(ValueError, "01_a question 1"):
            self.parse(GOOD.replace('"answer": 1', '"answer": 7'))

    def test_missing_stage_topic(self):
        with self.assertRaisesRegex(ValueError, "missing: 06_b"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', ''))

    def test_unknown_topic(self):
        with self.assertRaisesRegex(ValueError, "unknown: 99_nope"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q, Q], "99_nope": [Q, Q]'))

    def test_needs_exactly_two_questions(self):
        with self.assertRaisesRegex(ValueError, "06_b: needs exactly two"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q]'))

    def test_ready_needs_one_question_per_skill(self):
        with self.assertRaisesRegex(ValueError, "READY"):
            self.parse(GOOD.replace('"objects")', '"names")'))

    def test_output_question_needs_code(self):
        with self.assertRaisesRegex(ValueError, "06_b question 2"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q, dict(Q, output=True)]'))

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                server.parse_starting_check(Path(tmp) / "starting_check.py", TOPICS)


class Place(unittest.TestCase):
    ORDER = ["01_a", "02_b", "03_c", "04_d"]

    def test_all_right_places_out_everything_asked(self):
        r = server.place("python", {}, {"01_a": [True, True], "02_b": [True, True]}, self.ORDER)
        self.assertEqual(r, {"start": "03_c", "placed_out": ["01_a", "02_b"]})

    def test_a_miss_on_the_first_topic_starts_there(self):
        r = server.place("python", {}, {"01_a": [False], "02_b": [True, True]}, self.ORDER)
        self.assertEqual(r, {"start": "01_a", "placed_out": ["02_b"]})

    def test_topics_never_asked_are_not_placed_out(self):
        r = server.place("python", {}, {"01_a": [True, True], "02_b": [True, False]}, self.ORDER)
        self.assertEqual(r, {"start": "02_b", "placed_out": ["01_a"]})

    def test_stopping_before_any_answer_starts_at_the_beginning(self):
        self.assertEqual(server.place("dsa", {}, {}, self.ORDER), {"start": "01_a", "placed_out": []})

    def test_everything_placed_out_has_no_start(self):
        answers = {t: [True] for t in self.ORDER}
        self.assertEqual(server.place("dsa", {}, answers, self.ORDER), {"start": None, "placed_out": self.ORDER})


class RecordPlacement(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = server.PROGRESS_FILE, server.WORKSPACE
        server.WORKSPACE = Path(self.tmp.name)
        server.PROGRESS_FILE = server.WORKSPACE / "progress.json"

    def tearDown(self):
        server.PROGRESS_FILE, server.WORKSPACE = self.old
        self.tmp.cleanup()

    def test_not_taken_by_default(self):
        self.assertIsNone(server.load_progress()["placement"])

    def test_stores_door_date_and_result(self):
        p = server.record_placement("python", {"names": True},
                                    {"01_big_o_in_practice": [True, True], "02_python_toolkit": [False]})["placement"]
        self.assertEqual(p["door"], "python")
        self.assertEqual(p["ready"], {"names": True})
        self.assertEqual(p["placed_out"], ["01_big_o_in_practice"])
        self.assertEqual(p["start"], "02_python_toolkit")
        self.assertRegex(p["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_skip_and_new_store_only_door_and_date(self):
        self.assertEqual(set(server.record_placement("skip")["placement"]), {"door", "date"})
        self.assertEqual(server.record_placement("new")["placement"]["door"], "new")

    def test_retake_replaces_the_old_result(self):
        server.record_placement("dsa", {}, {"01_big_o_in_practice": [True], "12_stacks": [True]})
        p = server.record_placement("python", {}, {"01_big_o_in_practice": [False]})["placement"]
        self.assertEqual((p["door"], p["placed_out"], p["start"]), ("python", [], "01_big_o_in_practice"))

    def test_rejects_bad_input_without_touching_progress(self):
        before = server.load_progress()
        for args in (("expert",), ("python", {"names": "yes"}, {}), ("python", {"swimming": True}, {}),
                     ("python", {}, {"99_nope": [True]}), ("python", {}, {"30_number_theory": [True]}),
                     ("python", {}, {"12_stacks": [True, True, True]}), ("python", {}, {"12_stacks": []}),
                     ("python", {}, {"12_stacks": "true"}), ("python", {}, {"12_stacks": [1]})):
            with self.assertRaises(ValueError, msg=args):
                server.record_placement(*args)
        self.assertEqual(server.load_progress(), before)

    def test_reset_clears_placement(self):
        server.record_placement("skip")
        self.assertIsNone(server.reset_progress()["placement"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run** `python -m unittest tests.test_starting_check -v`. Expected: errors such as `AttributeError: module 'server' has no attribute 'parse_starting_check'`.

- [ ] **Step 3: Constants.** In `server.py`, directly after `PROGRESS_FILE = WORKSPACE / "progress.json"`:

```python
STARTING_CHECK = COURSE / "starting_check.py"
SKILLS = ("names", "loops", "functions", "lists", "dicts", "objects")    # the ready check asks one question each
DOORS = ("new", "python", "dsa", "skip")                                  # "Where are you starting?"
```

- [ ] **Step 4: The parser.** In `server.py`, directly after `load_walkthrough_safely`:

```python
def _check_question(q, where):
    """One multiple-choice question: question, 2-5 options, an answer index, an explanation; optional code."""
    if not isinstance(q, dict):
        raise ValueError(f"{where}: must be a dict")
    options, answer = q.get("options"), q.get("answer")
    if not q.get("question") or not q.get("explain") or not isinstance(options, list) \
            or not 2 <= len(options) <= 5 or type(answer) is not int or not 0 <= answer < len(options):
        raise ValueError(f"{where}: needs a question, 2-5 options, an answer index into them, and an explanation")
    if q.get("output") and not q.get("code"):
        raise ValueError(f"{where}: an output question needs code")
    return {"question": q["question"], "options": [str(o) for o in options], "answer": answer,
            "explain": q["explain"], "code": textwrap.dedent(q.get("code") or "").strip("\n"),
            "output": bool(q.get("output"))}


def parse_starting_check(path, topics):
    """starting_check.py: READY (one Python question per skill) and TOPICS (two questions for every
    Stage 1-4 topic, the more telling one first). Raises FileNotFoundError if the file is missing."""
    module = load_module(path)
    ready, asked = module.get("READY"), module.get("TOPICS")
    skills = sorted(str(q.get("skill")) if isinstance(q, dict) else "" for q in ready) if isinstance(ready, list) else []
    if skills != sorted(SKILLS):
        raise ValueError(f"{path.name}: READY needs exactly one question for each skill: {', '.join(SKILLS)}")
    if not isinstance(asked, dict):
        raise ValueError(f"{path.name}: TOPICS must map topic ids to questions")
    expected = [t for t in topics if 1 <= t["stage_n"] <= 4]
    unknown = sorted(set(asked) - {t["id"] for t in expected})
    missing = [t["id"] for t in expected if t["id"] not in asked]
    if unknown or missing:
        raise ValueError(f"{path.name}: TOPICS must cover every Stage 1-4 topic"
                         + (f"; unknown: {', '.join(unknown)}" if unknown else "")
                         + (f"; missing: {', '.join(missing)}" if missing else ""))
    out = []
    for t in expected:
        qs = asked[t["id"]]
        if not isinstance(qs, list) or len(qs) != 2:
            raise ValueError(f"{path.name} {t['id']}: needs exactly two questions")
        out.append({"id": t["id"], "title": t["title"], "stage_n": t["stage_n"],
                    "questions": [_check_question(q, f"{path.name} {t['id']} question {i}") for i, q in enumerate(qs, 1)]})
    return {"ready": [{**_check_question(q, f"{path.name} READY {i}"), "skill": q["skill"]} for i, q in enumerate(ready, 1)],
            "topics": out}
```

- [ ] **Step 5: Placement and reset.** In `server.py`, directly after `record_walkthrough`:

```python
def place(door, ready, answers, topic_order):
    """Where a finished starting check puts you. A topic is placed out when at least one question about
    it was asked and every one asked was right; you start at the first topic that isn't placed out.
    (door and ready start to matter in Phase 4, when Stage 0 exists.)"""
    placed = [t for t in topic_order if answers.get(t) and all(answers[t])]
    return {"start": next((t for t in topic_order if t not in placed), None), "placed_out": placed}


def record_placement(door, ready=None, answers=None):
    """Validate a starting check and store where it puts you, replacing any earlier result."""
    if door not in DOORS:
        raise ValueError(f"door must be one of: {', '.join(DOORS)}")
    result = {"door": door, "date": time.strftime("%Y-%m-%d")}
    if door in ("python", "dsa"):
        ready, answers = {} if ready is None else ready, {} if answers is None else answers
        topics = load_course()[0]
        known = {t["id"] for t in topics if 1 <= t["stage_n"] <= 4}
        if not isinstance(ready, dict) or any(k not in SKILLS or type(v) is not bool for k, v in ready.items()):
            raise ValueError("ready must map skills to true or false")
        if not isinstance(answers, dict) or any(
                k not in known or not isinstance(v, list) or not 1 <= len(v) <= 2 or any(type(x) is not bool for x in v)
                for k, v in answers.items()):
            raise ValueError("answers must map Stage 1-4 topic ids to one or two true/false results")
        result |= {"ready": ready, **place(door, ready, answers, [t["id"] for t in topics])}

    def change(progress):
        progress["placement"] = result
    return update_progress(change)


def reset_progress():
    def wipe(progress):
        progress["problems"], progress["unlocked"], progress["walkthroughs"], progress["placement"] = {}, [], {}, None
    return update_progress(wipe)
```

- [ ] **Step 6: Default.** In `load_progress()`, after `progress.setdefault("walkthroughs", {})      # topic id -> layers answered`, add:

```python
    progress.setdefault("placement", None)        # where the starting check put you; None = not taken
```

- [ ] **Step 7: Routes.**
  - In `do_GET`, directly above `if route.startswith("/api/"):`, add:

```python
        if route == "/api/starting-check":
            try:
                return self.send_json(parse_starting_check(STARTING_CHECK, load_course()[0]))
            except FileNotFoundError:
                return self.fail("This course has no starting check", HTTPStatus.NOT_FOUND)
            except ValueError as exc:
                return self.fail(str(exc), HTTPStatus.INTERNAL_SERVER_ERROR)
```

  - In `do_POST`, replace the whole `/api/reset-progress` branch:

```python
        if route == "/api/reset-progress":
            def wipe(progress):
                progress["problems"], progress["unlocked"], progress["walkthroughs"] = {}, [], {}
            return self.send_json({"progress": update_progress(wipe)})
```

  with:

```python
        if route == "/api/reset-progress":
            return self.send_json({"progress": reset_progress()})

        if route == "/api/placement":
            try:
                progress = record_placement(data.get("door"), data.get("ready"), data.get("answers"))
            except ValueError as exc:
                return self.fail(str(exc))
            return self.send_json({"progress": progress})
```

- [ ] **Step 8: Run** `python -m unittest discover -s tests -v`. Expected: all pass.

- [ ] **Step 9: Commit**

```bash
git add server.py tests/test_starting_check.py
git commit -m "Starting check: parsing, placement and API" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 3: Starting check content and self-check

**Files:**
- Create: `course/starting_check.py`
- Modify: `server.py` (`check()`: validate the file and run its output questions)
- Modify: `tests/test_starting_check.py` (one real-file test)

**Interfaces:**
- Consumes: `parse_starting_check`, `STARTING_CHECK` (Task 2); `run_script(code) -> {"exit_code", "output", "killed", "seconds"}` (existing).
- Produces: the real check, 6 READY questions and 2 × 25 topic questions; `python server.py --check starting` validates it.

- [ ] **Step 1: Write the failing test.** Append to `tests/test_starting_check.py`, above the `if __name__` line:

```python
class RealFile(unittest.TestCase):
    def test_course_file_parses(self):
        check = server.parse_starting_check(server.STARTING_CHECK, server.load_course()[0])
        self.assertEqual(len(check["ready"]), 6)
        self.assertEqual(len(check["topics"]), 25)
        self.assertEqual(check["topics"][0]["id"], "01_big_o_in_practice")
```

- [ ] **Step 2: Run** `python -m unittest tests.test_starting_check.RealFile -v`. Expected: `FileNotFoundError`.

- [ ] **Step 3: Write the content** in `course/starting_check.py`, exactly:

```python
"""Where are you starting?

READY: one Python question per skill. Missing two or more suggests learning some Python first.
TOPICS: two questions for every Stage 1-4 topic, the more telling one first ("Done DSA" asks only that one).
A question marked "output": True must print exactly options[answer]: `python server.py --check starting`
runs every one of them.
"""

READY = [
    {
        "skill": "names",
        "question": "What does this print?",
        "code": """
            x = 3
            x = x + 2
            print(x)
        """,
        "options": ["3", "5", "x + 2"],
        "answer": 1,
        "explain": "The second line reads `x` (3), adds 2, and points `x` at the result, 5.",
        "output": True,
    },
    {
        "skill": "loops",
        "question": "What does this print?",
        "code": """
            total = 0
            for i in range(1, 5):
                if i % 2 == 0:
                    total += i
            print(total)
        """,
        "options": ["4", "6", "10", "2"],
        "answer": 1,
        "explain": "`range(1, 5)` gives 1, 2, 3, 4. Only 2 and 4 are even, so `total` ends at 6.",
        "output": True,
    },
    {
        "skill": "functions",
        "question": "What does this print?",
        "code": """
            def double(n):
                n * 2

            print(double(4))
        """,
        "options": ["8", "None", "4"],
        "answer": 1,
        "explain": "The function works out `n * 2` but never returns it, so the call gives `None`.",
        "output": True,
    },
    {
        "skill": "lists",
        "question": "What does this print?",
        "code": """
            nums = [10, 20, 30, 40]
            print(nums[1] + nums[-1])
        """,
        "options": ["30", "50", "60", "70"],
        "answer": 2,
        "explain": "Indexes start at 0, so `nums[1]` is 20, and `nums[-1]` is the last item, 40.",
        "output": True,
    },
    {
        "skill": "dicts",
        "question": "What does this print?",
        "code": """
            counts = {}
            for ch in "banana":
                counts[ch] = counts.get(ch, 0) + 1
            print(counts["a"])
        """,
        "options": ["1", "2", "3", "6"],
        "answer": 2,
        "explain": "`counts.get(ch, 0)` starts each letter at 0, and a appears three times in banana.",
        "output": True,
    },
    {
        "skill": "objects",
        "question": "What does this print?",
        "code": """
            class Node:
                def __init__(self, val):
                    self.val = val
                    self.next = None

            a = Node(1)
            b = Node(2)
            a.next = b
            print(a.next.val)
        """,
        "options": ["1", "2", "None", "an error"],
        "answer": 1,
        "explain": "`a.next` points at the node `b`, and `b.val` is 2.",
        "output": True,
    },
]

TOPICS = {
    "01_big_o_in_practice": [
        {
            "question": "How many times does `work()` run?",
            "code": """
                for i in range(n):
                    for j in range(i):
                        work()
            """,
            "options": ["n", "about n²/2", "n log n", "2n"],
            "answer": 1,
            "explain": "The inner loop runs 0, 1, 2, … n − 1 times: n(n − 1)/2 in all, which grows like n².",
        },
        {
            "question": "The input has up to 200,000 numbers. Which idea is fast enough?",
            "options": ["Compare every pair: O(n²)", "Sort, then one pass: O(n log n)", "Try every subset: O(2ⁿ)"],
            "answer": 1,
            "explain": "200,000² is 40 billion steps, far too many. n log n is a few million.",
        },
    ],
    "02_python_toolkit": [
        {
            "question": "Which line is O(n) on a list `a` of n items?",
            "options": ["`a.append(x)`", "`x in a`", "`a[i]`", "`a.pop()`"],
            "answer": 1,
            "explain": "Membership in a list checks items one by one. `append`, indexing and `pop()` from the end are O(1).",
        },
        {
            "question": "What does this print?",
            "code": """
                from collections import Counter
                print(Counter("hello").most_common(1))
            """,
            "options": ["[('l', 2)]", "[('h', 1)]", "{'l': 2}", "2"],
            "answer": 0,
            "explain": "`Counter` counts each letter, and `most_common(1)` returns the top `(item, count)` pair in a list.",
            "output": True,
        },
    ],
    "03_arrays_and_strings": [
        {
            "question": "What does this print?",
            "code": """
                a = [1, 2, 3, 4, 5]
                k = 2
                print(a[-k:] + a[:-k])
            """,
            "options": ["[4, 5, 1, 2, 3]", "[3, 4, 5, 1, 2]", "[1, 2, 3, 4, 5]"],
            "answer": 0,
            "explain": "`a[-2:]` is the last two items and `a[:-2]` is the rest: the list rotated right by 2.",
            "output": True,
        },
        {
            "question": "An array of length n is rotated right by k. Where does the item at index i end up?",
            "options": ["`(i + k) % n`", "`(i - k) % n`", "`i + k`", "`n - i - k`"],
            "answer": 0,
            "explain": "Every item moves k places right and wraps past the end, so the new index is taken modulo n.",
        },
    ],
    "04_hashing": [
        {
            "question": "In one pass over an unsorted list, you want to know whether any two numbers add up to "
                        "`target`. What do you keep as you go?",
            "options": ["The numbers seen so far, in a set", "The list, sorted", "Every pair's sum", "Only the previous number"],
            "answer": 0,
            "explain": "For each x, check whether `target - x` is already in the set, then add x. Each check is O(1).",
        },
        {
            "question": "What does this print?",
            "code": """
                groups = {}
                for w in ["eat", "tea", "tan"]:
                    key = "".join(sorted(w))
                    groups.setdefault(key, []).append(w)
                print(len(groups))
            """,
            "options": ["1", "2", "3"],
            "answer": 1,
            "explain": "Sorted letters make a key that anagrams share: eat and tea both give aet, while tan gives ant.",
            "output": True,
        },
    ],
    "05_recursion": [
        {
            "question": "What does this print?",
            "code": """
                def f(n):
                    if n == 0:
                        return 0
                    return n + f(n - 1)

                print(f(4))
            """,
            "options": ["4", "10", "24", "an error"],
            "answer": 1,
            "explain": "f(4) = 4 + f(3) = 4 + 3 + 2 + 1 + 0 = 10.",
            "output": True,
        },
        {
            "question": "What happens if you delete the `if n == 0` check from `f`?",
            "options": ["It returns 0", "It calls itself until Python stops it with a RecursionError",
                        "It returns n", "It runs once and stops"],
            "answer": 1,
            "explain": "Without a base case nothing stops the calls. Python gives up after about 1,000 levels.",
        },
    ],
    "06_two_pointers": [
        {
            "question": "Find two numbers in a sorted array that add up to `target`, in O(n) time and O(1) extra "
                        "space. How?",
            "options": ["A pointer at each end: move the left one right if the sum is too small, the right one left if it's too big",
                        "Store every number in a set", "Check every pair", "Sort the array again first"],
            "answer": 0,
            "explain": "The sorted order tells you which pointer to move, and each one only moves inward: one pass, no extra memory.",
        },
        {
            "question": "What does this print?",
            "code": """
                s = "racecar"
                i, j = 0, len(s) - 1
                while i < j and s[i] == s[j]:
                    i += 1
                    j -= 1
                print(i >= j)
            """,
            "options": ["True", "False"],
            "answer": 0,
            "explain": "The pointers meet in the middle without finding a mismatch, so racecar reads the same both ways.",
            "output": True,
        },
    ],
    "07_sliding_window": [
        {
            "question": "Longest substring with no repeated letter: `right` moves forward one letter at a time. "
                        "When does `left` move?",
            "options": ["While the window holds a repeated letter", "Every step", "Never", "Only when `right` reaches the end"],
            "answer": 0,
            "explain": "Shrink from the left until the window is valid again (no repeats), then record its length.",
        },
        {
            "question": "What does this print?",
            "code": """
                nums = [2, 1, 5, 1, 3, 2]
                k = 3
                window = sum(nums[:k])
                best = window
                for i in range(k, len(nums)):
                    window += nums[i] - nums[i - k]
                    best = max(best, window)
                print(best)
            """,
            "options": ["8", "9", "10", "14"],
            "answer": 1,
            "explain": "Each step adds the item coming in and drops the one leaving: the window sums are 8, 7, 9, 6.",
            "output": True,
        },
    ],
    "08_prefix_sums": [
        {
            "question": "What does this print?",
            "code": """
                nums = [3, 1, 4, 1, 5]
                prefix = [0]
                for x in nums:
                    prefix.append(prefix[-1] + x)
                print(prefix[4] - prefix[1])
            """,
            "options": ["6", "5", "9", "10"],
            "answer": 0,
            "explain": "`prefix[i]` is the sum of the first i items, so `prefix[4] - prefix[1]` is 1 + 4 + 1 = 6.",
            "output": True,
        },
        {
            "question": "Count the subarrays that sum to k when the array has negative numbers. What works in O(n)?",
            "options": ["A running sum, plus a dict counting how often each running sum has appeared",
                        "A sliding window", "Sorting first, then two pointers", "Checking every subarray"],
            "answer": 0,
            "explain": "Negative numbers break a window's grow-and-shrink logic. A subarray ending here sums to k exactly "
                       "when `running - k` appeared before.",
        },
    ],
    "09_binary_search": [
        {
            "question": "What does this print?",
            "code": """
                from bisect import bisect_left
                print(bisect_left([1, 3, 5, 7], 6))
            """,
            "options": ["2", "3", "4"],
            "answer": 1,
            "explain": "6 belongs just before 7, which is at index 3.",
            "output": True,
        },
        {
            "question": "Find the smallest eating speed that finishes every pile within h hours. Why can you "
                        "binary search the speed?",
            "options": ["If a speed works, every faster speed works too", "The piles are sorted",
                        "The speeds are small numbers", "Each pile takes one hour"],
            "answer": 0,
            "explain": "The check 'finishes in time' flips from no to yes once as the speed grows, so binary search finds the first yes.",
        },
    ],
    "10_sorting_and_intervals": [
        {
            "question": "What does this print?",
            "code": """
                intervals = [[1, 3], [8, 10], [2, 6]]
                intervals.sort()
                merged = [intervals[0]]
                for start, end in intervals[1:]:
                    if start <= merged[-1][1]:
                        merged[-1][1] = max(merged[-1][1], end)
                    else:
                        merged.append([start, end])
                print(merged)
            """,
            "options": ["[[1, 6], [8, 10]]", "[[1, 3], [2, 6], [8, 10]]", "[[1, 10]]"],
            "answer": 0,
            "explain": "After sorting by start, [2, 6] overlaps [1, 3] and stretches it to [1, 6]. [8, 10] starts after 6.",
            "output": True,
        },
        {
            "question": "What does this print?",
            "code": """
                people = [("ann", 30), ("bob", 25), ("cy", 30)]
                print(sorted(people, key=lambda p: (-p[1], p[0]))[0][0])
            """,
            "options": ["ann", "bob", "cy"],
            "answer": 0,
            "explain": "The key sorts by age, oldest first (`-p[1]`), and breaks ties by name, so ann comes before cy.",
            "output": True,
        },
    ],
    "11_greedy": [
        {
            "question": "Each value is your maximum jump length. To decide whether you can reach the last index, "
                        "what is enough to track?",
            "options": ["The farthest index you can reach so far", "Every path you could take",
                        "The number of jumps made", "The smallest value seen"],
            "answer": 0,
            "explain": "Walk left to right. If i is ever past the farthest reach you're stuck; otherwise update it with i + nums[i].",
        },
        {
            "question": "Coins are 1, 3 and 4, and the amount is 6. Always taking the biggest coin gives 4 + 1 + 1. "
                        "What's the fewest coins possible?",
            "options": ["2", "3", "4"],
            "answer": 0,
            "explain": "3 + 3 uses two coins. Taking the biggest coin first isn't always best; this problem needs DP.",
        },
    ],
    "12_stacks": [
        {
            "question": "What does this print?",
            "code": """
                stack = []
                for ch in "(()":
                    if ch == "(":
                        stack.append(ch)
                    elif stack:
                        stack.pop()
                print(len(stack))
            """,
            "options": ["0", "1", "2"],
            "answer": 1,
            "explain": "Two opening brackets and one closing bracket leave one unmatched `(` on the stack.",
            "output": True,
        },
        {
            "question": "For each day's temperature, find how many days until a warmer one. What gives O(n)?",
            "options": ["A stack of days still waiting for a warmer day", "A queue of every day",
                        "Sorting the temperatures", "A dict from temperature to day"],
            "answer": 0,
            "explain": "Each day is pushed once and popped once, when a warmer day arrives: a monotonic stack.",
        },
    ],
    "13_queues_and_deques": [
        {
            "question": "What does this print?",
            "code": """
                from collections import deque
                q = deque([1, 2, 3])
                q.append(4)
                q.popleft()
                print(q[0])
            """,
            "options": ["1", "2", "4"],
            "answer": 1,
            "explain": "`popleft()` removes the front item, 1, so 2 is now at the front.",
            "output": True,
        },
        {
            "question": "Why use `deque.popleft()` rather than `list.pop(0)` for a queue?",
            "options": ["`popleft()` is O(1); `pop(0)` shifts every remaining item, O(n)", "`pop(0)` removes the last item",
                        "A list can't hold more than 1,000 items", "They take the same time"],
            "answer": 0,
            "explain": "After `pop(0)` a list moves every remaining item one place left. A deque doesn't have to.",
        },
    ],
    "14_linked_lists": [
        {
            "question": "What does this print?",
            "code": """
                class ListNode:
                    def __init__(self, val, next=None):
                        self.val = val
                        self.next = next

                head = ListNode(1, ListNode(2, ListNode(3)))
                prev, node = None, head
                while node:
                    nxt = node.next
                    node.next = prev
                    prev = node
                    node = nxt
                print(prev.val)
            """,
            "options": ["1", "3", "None"],
            "answer": 1,
            "explain": "The loop reverses the links one node at a time. At the end `prev` is the old tail, 3: the new head.",
            "output": True,
        },
        {
            "question": "How do you find the middle node of a linked list in one pass?",
            "options": ["Move one pointer one step and another two steps at a time; when the fast one reaches the end, the slow one is in the middle",
                        "Binary search on the nodes", "Reverse it, then walk to the middle", "Jump straight to index n // 2"],
            "answer": 0,
            "explain": "Fast and slow pointers: the slow one has always gone half as far as the fast one.",
        },
    ],
    "15_trees": [
        {
            "question": "What does this print?",
            "code": """
                class TreeNode:
                    def __init__(self, val, left=None, right=None):
                        self.val, self.left, self.right = val, left, right

                def depth(node):
                    if node is None:
                        return 0
                    return 1 + max(depth(node.left), depth(node.right))

                root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
                print(depth(root))
            """,
            "options": ["2", "3", "4"],
            "answer": 1,
            "explain": "The longest path from the root is 1 → 2 → 4: three nodes.",
            "output": True,
        },
        {
            "question": "Which traversal visits a tree level by level?",
            "options": ["Breadth-first, with a queue", "Pre-order recursion", "In-order recursion", "Post-order recursion"],
            "answer": 0,
            "explain": "A queue hands out every node at depth d before any node at depth d + 1.",
        },
    ],
    "16_binary_search_trees": [
        {
            "question": "What does an in-order traversal of a binary search tree give you?",
            "options": ["The values in sorted order", "The values level by level",
                        "The values in the order they were inserted", "Only the leaves"],
            "answer": 0,
            "explain": "Left subtree < node < right subtree, so visiting left, node, right goes through the values in increasing order.",
        },
        {
            "question": "What does this print?",
            "code": """
                class Node:
                    def __init__(self, val):
                        self.val, self.left, self.right = val, None, None

                def insert(node, val):
                    if node is None:
                        return Node(val)
                    if val < node.val:
                        node.left = insert(node.left, val)
                    else:
                        node.right = insert(node.right, val)
                    return node

                root = None
                for v in [5, 3, 8, 1]:
                    root = insert(root, v)
                print(root.left.left.val)
            """,
            "options": ["1", "3", "8"],
            "answer": 0,
            "explain": "1 is smaller than 5 and then smaller than 3, so it becomes 3's left child.",
            "output": True,
        },
    ],
    "17_heaps": [
        {
            "question": "What does this print?",
            "code": """
                import heapq
                h = [5, 1, 8, 3]
                heapq.heapify(h)
                heapq.heappush(h, 0)
                print(heapq.heappop(h), heapq.heappop(h))
            """,
            "options": ["0 1", "8 5", "5 1", "0 3"],
            "answer": 0,
            "explain": "`heapq` is a min-heap: each pop returns the smallest item left.",
            "output": True,
        },
        {
            "question": "You keep the k largest of n numbers with a min-heap of size k. What does it cost?",
            "options": ["O(n log k)", "O(n²)", "O(k²)", "O(n)"],
            "answer": 0,
            "explain": "Each number costs at most one push and one pop on a heap of size k, which is O(log k).",
        },
    ],
    "18_tries": [
        {
            "question": "Why use a trie for autocomplete instead of a list of words?",
            "options": ["Words that share a prefix share a path, so every word with a prefix sits under one node",
                        "It always uses less memory than a list", "It keeps words in the order they were added",
                        "It finds any word in O(1), however long"],
            "answer": 0,
            "explain": "Walk the prefix's letters once; everything below that node starts with the prefix.",
        },
        {
            "question": "What does this print?",
            "code": """
                trie = {}
                for word in ["car", "cat", "dog"]:
                    node = trie
                    for ch in word:
                        node = node.setdefault(ch, {})
                print(len(trie), len(trie["c"]["a"]))
            """,
            "options": ["2 2", "3 2", "2 1", "3 3"],
            "answer": 0,
            "explain": "car and cat share c → a, then split into r and t. dog starts its own branch, so the root has two children.",
            "output": True,
        },
    ],
    "19_graph_traversal": [
        {
            "question": "Find the fewest moves from start to target on a grid where every move costs the same. "
                        "Which search?",
            "options": ["Breadth-first search (BFS)", "Depth-first search (DFS)", "Trying every path", "Sorting the cells first"],
            "answer": 0,
            "explain": "BFS explores in rings of distance 1, 2, 3 and so on, so it first reaches the target along a shortest path.",
        },
        {
            "question": "What does this print?",
            "code": """
                grid = ["11000",
                        "11000",
                        "00100",
                        "00011"]
                seen = set()

                def flood(r, c):
                    if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
                        return
                    if grid[r][c] == "0" or (r, c) in seen:
                        return
                    seen.add((r, c))
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        flood(r + dr, c + dc)

                islands = 0
                for r in range(len(grid)):
                    for c in range(len(grid[0])):
                        if grid[r][c] == "1" and (r, c) not in seen:
                            flood(r, c)
                            islands += 1
                print(islands)
            """,
            "options": ["2", "3", "4", "5"],
            "answer": 1,
            "explain": "Each flood marks one whole island: the 2×2 block, the single cell, and the pair at the bottom right. "
                       "Diagonals don't connect.",
            "output": True,
        },
    ],
    "20_topological_sort_and_union_find": [
        {
            "question": "Courses have prerequisites. How do you tell whether every course can be finished?",
            "options": ["Look for a cycle in the prerequisite graph, for example with a topological sort",
                        "Sort the courses by number", "Count the courses", "Take the course with the most prerequisites first"],
            "answer": 0,
            "explain": "A cycle means some course depends on itself. A topological sort can order every course only if there's no cycle.",
        },
        {
            "question": "What does this print?",
            "code": """
                parent = list(range(5))

                def find(x):
                    while parent[x] != x:
                        x = parent[x]
                    return x

                def union(a, b):
                    parent[find(a)] = find(b)

                union(0, 1)
                union(3, 4)
                union(1, 4)
                print(find(0) == find(3), find(2) == find(0))
            """,
            "options": ["True False", "False False", "True True", "False True"],
            "answer": 0,
            "explain": "0 joins 1, 3 joins 4, then 1 joins 4, so 0 and 3 end up in one group. 2 never joins anything.",
            "output": True,
        },
    ],
    "21_weighted_graphs": [
        {
            "question": "Find the shortest travel time when roads take different (positive) amounts of time. "
                        "What do you use?",
            "options": ["Dijkstra's algorithm with a min-heap", "Plain BFS", "DFS", "Union-find"],
            "answer": 0,
            "explain": "BFS counts roads, not time. Dijkstra always settles the closest unfinished place next.",
        },
        {
            "question": "What does this print?",
            "code": """
                import heapq
                graph = {"a": [("b", 4), ("c", 1)], "c": [("b", 2)], "b": []}
                dist = {"a": 0}
                heap = [(0, "a")]
                while heap:
                    d, node = heapq.heappop(heap)
                    if d > dist[node]:
                        continue
                    for nxt, w in graph[node]:
                        if d + w < dist.get(nxt, float("inf")):
                            dist[nxt] = d + w
                            heapq.heappush(heap, (d + w, nxt))
                print(dist["b"])
            """,
            "options": ["3", "4", "6"],
            "answer": 0,
            "explain": "Going a → c → b costs 1 + 2 = 3, less than the direct road of 4.",
            "output": True,
        },
    ],
    "22_backtracking": [
        {
            "question": "What does this print?",
            "code": """
                out = []

                def build(path, rest):
                    if not rest:
                        out.append(path)
                        return
                    for i in range(len(rest)):
                        build(path + rest[i], rest[:i] + rest[i + 1:])

                build("", "abc")
                print(len(out))
            """,
            "options": ["3", "6", "8", "9"],
            "answer": 1,
            "explain": "3 choices for the first letter, 2 for the second and 1 for the last: 3 × 2 × 1 = 6 orderings.",
            "output": True,
        },
        {
            "question": "How many subsets does a set of n distinct numbers have?",
            "options": ["2ⁿ", "n²", "n!", "n"],
            "answer": 0,
            "explain": "Each number is either in or out: two choices, made n times.",
        },
    ],
    "23_dynamic_programming_1d": [
        {
            "question": "What does this print?",
            "code": """
                from functools import cache

                @cache
                def ways(n):
                    if n <= 1:
                        return 1
                    return ways(n - 1) + ways(n - 2)

                print(ways(5))
            """,
            "options": ["5", "8", "13", "10"],
            "answer": 1,
            "explain": "The last step was 1 or 2 stairs, so ways(n) = ways(n − 1) + ways(n − 2): 1, 1, 2, 3, 5, 8.",
            "output": True,
        },
        {
            "question": "Adding `@cache` to a recursive function like `ways` changes its running time from…",
            "options": ["O(2ⁿ) to O(n)", "O(n) to O(1)", "O(n²) to O(n log n)", "Nothing; it only saves memory"],
            "answer": 0,
            "explain": "Without memoisation the same subproblems are recomputed exponentially often. With it, each `ways(k)` is worked out once.",
        },
    ],
    "24_dynamic_programming_2d": [
        {
            "question": "What does this print?",
            "code": """
                m, n = 3, 3
                paths = [[1] * n for _ in range(m)]
                for r in range(1, m):
                    for c in range(1, n):
                        paths[r][c] = paths[r - 1][c] + paths[r][c - 1]
                print(paths[m - 1][n - 1])
            """,
            "options": ["4", "6", "9"],
            "answer": 1,
            "explain": "Paths to a cell = paths from above + paths from the left. The bottom-right corner of a 3×3 grid gets 6.",
            "output": True,
        },
        {
            "question": "For the longest common subsequence of strings a and b, what does `dp[i][j]` usually stand for?",
            "options": ["The answer for the first i letters of a and the first j letters of b", "Whether `a[i]` equals `b[j]`",
                        "How many letters a and b have in common anywhere", "Where `a[i]` appears in b"],
            "answer": 0,
            "explain": "Subproblems on prefixes let each cell build on `dp[i-1][j-1]`, `dp[i-1][j]` and `dp[i][j-1]`.",
        },
    ],
    "25_bit_tricks": [
        {
            "question": "What does this print?",
            "code": """
                nums = [4, 1, 2, 1, 2]
                x = 0
                for v in nums:
                    x ^= v
                print(x)
            """,
            "options": ["0", "4", "10", "1"],
            "answer": 1,
            "explain": "XOR cancels pairs (a ^ a is 0), leaving the number that appears once.",
            "output": True,
        },
        {
            "question": "What does this print?",
            "code": """
                print(bin(12), 12 & (12 - 1))
            """,
            "options": ["0b1100 8", "0b1100 11", "0b1010 8", "0b1100 4"],
            "answer": 0,
            "explain": "`n & (n - 1)` clears the lowest set bit: 1100 becomes 1000, which is 8.",
            "output": True,
        },
    ],
}
```

- [ ] **Step 4: Teach `--check` about it.** In `server.py`, inside `check()`, directly above `print("\nAll good." if not failures else f"\n{failures} problem(s).")`, add:

```python
    if not only or any(o in "starting_check" for o in only):
        label = "starting check"
        try:
            sc = parse_starting_check(STARTING_CHECK, topics)
        except (ValueError, FileNotFoundError) as exc:
            failures += 1
            print(f"  FAIL {label:<50} {exc}")
        else:
            questions = [(f"READY {q['skill']}", q) for q in sc["ready"]] + \
                        [(f"{t['id']} question {i}", q) for t in sc["topics"] for i, q in enumerate(t["questions"], 1)]
            bad = []
            for where, q in questions:
                if q["output"]:
                    run = run_script(q["code"])
                    got, want = (run["output"] or "").strip(), q["options"][q["answer"]].strip()
                    if run["exit_code"] != 0 or run["killed"] or got != want:
                        bad.append(f"{where}: printed {got!r}, but the answer says {want!r}")
            failures += bool(bad)
            print(f"  {'FAIL' if bad else 'ok  '} {label:<50} {len(questions):>2} questions")
            for line in bad:
                print("        ", line)
```

- [ ] **Step 5: Run** `python -m unittest discover -s tests -v`, then `python server.py --check starting`. Expected: all tests pass. `--check` prints `ok   starting check   56 questions` and `All good.` If an output question fails, fix that question's `options`/`answer` (never the check) and re-run.

- [ ] **Step 6: Commit**

```bash
git add course/starting_check.py server.py tests/test_starting_check.py
git commit -m "Starting check questions, verified by --check" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 4: "Where are you starting?" screen

**Files:**
- Create: `web/start.js`
- Modify: `web/index.html` (load `start.js`)
- Modify: `web/app.js` (helpers, `viewStart`, route, first-visit redirect)
- Modify: `web/app.css` (start-page styles)

**Interfaces:**
- Consumes: `GET /api/starting-check` and `POST /api/placement` (Task 2); `topic.stage_n` (Task 1).
- Produces:
  - `T.mountStart(container, check, {place, topicTitle, startHref}) -> {unmount()}`, where:
    - `place(payload)` POSTs to `/api/placement` and resolves to the new progress;
    - `topicTitle(id)` gives a topic's display title;
    - `startHref(id)` gives the hash of a topic's first step.
  - `app.js` helpers `firstStep(topic) -> string` (hash) and `firstVisit() -> boolean`.

- [ ] **Step 1: Write `web/start.js`**:

```js
"use strict";
/* "Where are you starting?": three doors, a short adaptive check, and where it places you. */
(function () {
  const T = window.Trace;
  const { h } = T;

  const COURSES = [
    ["The official Python tutorial", "https://docs.python.org/3/tutorial/"],
    ["Harvard's CS50P", "https://cs50.harvard.edu/python/"],
    ["Python for Everybody", "https://www.py4e.com/"],
  ];
  const SKILLS = [
    "Give names to values and change them",
    "Use if/else and loops (for, while, range)",
    "Write functions that return a result",
    "Index, slice and loop over lists",
    "Count and look things up with a dict",
    "Make a small class and follow references between objects",
  ];

  // check: the /api/starting-check payload. place(payload) -> Promise of the new progress.
  T.mountStart = function mountStart(container, check, { place, topicTitle, startHref }) {
    let door = null, gen = null, count = 0, busy = false;
    let ready = {}, answers = {};

    function page(...kids) {
      container.replaceChildren(...kids.flat(Infinity).filter(Boolean));
      const scroller = container.closest("#app");
      if (scroller) scroller.scrollTop = 0;
    }

    function doors() {
      const choice = (id, title, sub) => h("button", { class: "door", type: "button", onclick: () => begin(id) },
        h("strong", {}, title), h("span", {}, sub));
      page(h("h1", {}, "Where are you starting?"),
        h("p", { class: "lede" }, "Pick the closest. A few questions find where to begin, and every topic stays open whatever you choose."),
        h("div", { class: "doors" },
          choice("new", "I'm new to programming", "Start from the very beginning."),
          choice("python", "I can write some Python", "Six Python questions, then the first two stages."),
          choice("dsa", "I've done DSA before", "One question per topic, to find your gaps.")),
        h("p", { class: "start-skip" }, h("button", { class: "link", type: "button", onclick: () => finish("skip") }, "I can program, show me everything")));
    }

    function begin(id) {
      if (id === "new") return finish("new");
      door = id;
      count = 0;
      ready = {};
      answers = {};
      gen = flow(id);
      step(undefined);
    }

    // Yields one question (or the "learn Python first?" screen) at a time; receives true/false back.
    function* flow(id) {
      if (id === "python") {
        let missed = 0;
        for (const q of check.ready) {
          ready[q.skill] = yield { label: "Python basics", q };
          if (!ready[q.skill]) missed++;
        }
        if (missed >= 2 && !(yield { suggest: missed })) return "new";
      }
      let failed = 0;
      for (const t of check.topics) {
        if (id === "python" && t.stage_n > 2) break;
        const label = topicTitle(t.id);
        const got = [yield { label, q: t.questions[0] }];
        if (got[0] && id === "python") got.push(yield { label, q: t.questions[1] });
        answers[t.id] = got;
        if (id === "python" && !got.every(Boolean) && ++failed >= 2) break;
      }
      return "done";
    }

    function step(value) {
      const r = gen.next(value);
      if (r.done) return finish(r.value === "new" ? "new" : door);
      if (r.value.suggest) return suggest(r.value.suggest);
      question(r.value);
    }

    function question({ label, q }) {
      count++;
      let answered = null;
      const explain = h("p", { class: "wt-explain", "aria-live": "polite", hidden: true });
      const next = h("button", { class: "btn primary", type: "button", disabled: true, onclick: () => step(answered) }, "Continue");
      const opts = q.options.map((text, k) => h("button", { type: "button", class: "opt", "data-i": k, onclick: () => choose(k) },
        h("kbd", {}, k + 1), h("span", {}, T.inline(text))));
      function choose(k) {
        if (answered !== null) return;
        answered = k === q.answer;
        opts.forEach((b, j) => {
          b.disabled = true;
          if (j === q.answer) b.classList.add("right");
          else if (j === k) b.classList.add("wrong");
        });
        explain.hidden = false;
        explain.className = "wt-explain " + (answered ? "ok" : "bad");
        explain.replaceChildren(h("strong", {}, answered ? "Right. " : "Not quite. "), ...T.inline(q.explain));
        next.disabled = false;
        next.focus({ preventScroll: true });
      }
      page(h("p", { class: "start-label" }, `${label}, question ${count}`),
        q.code ? h("pre", { class: "start-code" }, q.code) : null,
        h("section", { class: "wt-check" }, h("p", { class: "wt-q" }, T.inline(q.question)), h("div", { class: "wt-opts" }, opts), explain),
        h("nav", { class: "wt-nav" }, h("button", { class: "link", type: "button", onclick: () => finish(door) }, "Stop here"), next));
    }

    function suggest(missed) {
      page(h("p", { class: "start-label" }, "Python basics"),
        h("h1", {}, `You missed ${missed} of the ${check.ready.length} Python questions`),
        h("p", { class: "lede" }, "Trace expects you to read and write small Python programs. A short Python course first might help more, but it's your call."),
        h("div", { class: "start-actions" },
          h("button", { class: "btn primary", type: "button", onclick: () => step(false) }, "Show me where to learn Python"),
          h("button", { class: "btn", type: "button", onclick: () => step(true) }, "Continue anyway")));
    }

    async function finish(chosen) {
      if (busy) return;
      busy = true;
      try {
        const progress = await place(chosen === "new" || chosen === "skip" ? { door: chosen } : { door: chosen, ready, answers });
        if (chosen === "skip") location.hash = "#/";
        else if (chosen === "new") newcomer();
        else result(progress.placement);
      } catch (err) {
        page(h("h1", {}, "That didn't save"), h("p", { class: "lede" }, err.message),
          h("div", { class: "start-actions" },
            h("button", { class: "btn primary", type: "button", onclick: () => finish(chosen) }, "Try again"),
            h("a", { class: "link", href: "#/" }, "Go to the topics")));
      } finally {
        busy = false;
      }
    }

    function newcomer() {
      page(h("h1", {}, "Start with Python"),
        h("p", { class: "lede" }, "Trace teaches data structures and algorithms in Python, so it expects you to read and write small programs first. You're ready when you can:"),
        h("ul", { class: "start-list" }, SKILLS.map((s) => h("li", {}, s))),
        h("p", { class: "start-note" }, "These free courses teach exactly that:"),
        h("ul", { class: "start-list" }, COURSES.map(([name, url]) =>
          h("li", {}, h("a", { class: "link", href: url, target: "_blank", rel: "noopener" }, name)))),
        h("div", { class: "start-actions" },
          h("button", { class: "btn primary", type: "button", onclick: () => begin("python") }, "Take the ready check"),
          h("a", { class: "link", href: "#/" }, "Look around first")));
    }

    function result(placement) {
      const placed = placement.placed_out || [];
      page(h("h1", {}, placement.start ? "Here's where to start" : "You placed out of everything we asked about"),
        placement.start ? h("p", { class: "lede" }, "Start with ", h("strong", {}, topicTitle(placement.start)), ".") : null,
        placed.length ? [h("p", { class: "start-label" }, "Placed out (still open any time)"),
          h("ul", { class: "start-list" }, placed.map((id) => h("li", {}, topicTitle(id))))] : null,
        h("div", { class: "start-actions" },
          h("a", { class: "btn primary", href: placement.start ? startHref(placement.start) : "#/" }, placement.start ? "Start here" : "Go to the topics"),
          placement.start ? h("a", { class: "link", href: "#/" }, "See all topics") : null));
    }

    function onKey(e) {
      if (e.ctrlKey || e.metaKey || e.altKey || e.target.matches?.("input, select, textarea")) return;
      if (/^[1-9]$/.test(e.key)) {
        const btn = container.querySelector(`.wt-opts [data-i="${Number(e.key) - 1}"]`);
        if (btn && !btn.disabled) { e.preventDefault(); btn.click(); }
      } else if (e.key === "Enter" && !e.target.matches?.("button, a")) {
        const btn = container.querySelector(".wt-nav .btn.primary");
        if (btn && !btn.disabled) { e.preventDefault(); btn.click(); }
      }
    }
    document.addEventListener("keydown", onKey);

    doors();
    return { unmount: () => document.removeEventListener("keydown", onKey) };
  };
})();
```

- [ ] **Step 2: Load it.** In `web/index.html`, after `<script src="walkthrough.js"></script>`, add `<script src="start.js"></script>` (still before `app.js`).

- [ ] **Step 3: Helpers.** In `web/app.js`, directly after the line that starts `const kindLabel = (p) =>`, add:

```js
  function firstStep(topic) {
    const dt = drillTopic(topic);
    if (dt) return `#/d/${dt.id}/${dt.drills[0].id}`;
    if (topic.has_walkthrough) return `#/w/${topic.id}`;
    return topic.items.length ? `#/p/${topic.items[0]}` : `#/t/${topic.id}`;
  }
  // Nothing done yet and no starting check taken: the first visit, which opens "Where are you starting?".
  function firstVisit() {
    const p = S.progress;
    if (p.placement || Object.keys(p.problems || {}).length || (p.unlocked || []).length || Object.keys(p.walkthroughs || {}).length) return false;
    return !T.topics.some((dt) => dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0));
  }
```

- [ ] **Step 4: The view.** In `web/app.js`, directly above `function viewHome() {`, add:

```js
  async function viewStart() {
    document.title = "Where are you starting? | Trace";
    crumbs({ label: "Topics", href: "#/" }, { label: "Where are you starting?" });
    const host = h("div", { class: "start-page", "aria-busy": "true" }, sk("sk-title"), sk("sk-line", "width:70%"));
    app.replaceChildren(host);
    let check;
    try {
      check = await api("/api/starting-check");
    } catch (err) {
      host.removeAttribute("aria-busy");
      host.replaceChildren(h("h1", {}, "The starting check isn't available"), h("p", { class: "lede" }, err.message),
        h("div", { class: "start-actions" }, h("a", { class: "btn primary", href: "#/" }, "Go to the topics")));
      return;
    }
    if (!host.isConnected) return;               // you navigated away while it loaded
    host.removeAttribute("aria-busy");
    const find = (id) => S.topics.find((t) => t.id === id);
    const m = T.mountStart(host, check, {
      place: async (payload) => (S.progress = (await api("/api/placement", payload)).progress),
      topicTitle: (id) => (find(id) ? topicTitle(find(id)) : id),
      startHref: (id) => (find(id) ? firstStep(find(id)) : "#/"),
    });
    S.cleanup = () => m.unmount();
  }
```

- [ ] **Step 5: Route and redirect.** In `route()`, replace

```js
      if (kind === "w") return await viewWalkthrough(a);
      return viewHome();
```

  with

```js
      if (kind === "w") return await viewWalkthrough(a);
      if (kind === "start") return await viewStart();
      if (!kind && firstVisit()) { history.replaceState(null, "", "#/start"); return await viewStart(); }
      return viewHome();
```

- [ ] **Step 6: Styles.** Append to `web/app.css`:

```css
/* ── Where are you starting? ─────────────────────────── */
.start-page { max-width: 760px; margin: 0 auto; padding: 48px 24px 96px; font-size: 16.5px; line-height: 1.6; }
.start-page h1 { font-size: 36px; line-height: 1.12; letter-spacing: -0.03em; margin: 0; font-weight: 700; }
.doors { display: grid; gap: 10px; margin-top: 28px; }
.door { display: grid; gap: 2px; width: 100%; padding: 18px 20px; border: 0; border-radius: var(--radius); background: var(--fill); text-align: left; cursor: pointer; }
.door:hover { background: var(--fill-2); }
.door strong { font-size: 17px; font-weight: 600; }
.door span { color: var(--ink-2); font-size: 15px; }
.start-skip { margin-top: 18px; }
.start-label { margin: 26px 0 0; font-size: 13.5px; font-weight: 600; color: var(--accent); }
.start-code { margin: 14px 0 0; padding: 14px 18px; background: var(--fill); border-radius: var(--radius); font: 14px/1.7 var(--mono); white-space: pre; overflow-x: auto; }
.start-list { margin: 12px 0 0; padding-left: 22px; color: var(--ink-2); }
.start-list li { margin: 4px 0; }
.start-note { margin: 22px 0 0; color: var(--ink-2); }
.start-actions { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-top: 28px; }
@media (max-width: 900px) { .start-page { padding: 28px 16px 72px; } .start-page h1 { font-size: 28px; } }
```

- [ ] **Step 7: Syntax check** with `node --check web/start.js && node --check web/app.js`. Expected: no output.

- [ ] **Step 8: Manual: each route through the check.** Start a server on an empty workspace and a port you haven't used, so localStorage is empty too:
  `TRACE_WORKSPACE="$(python -c 'import tempfile; print(tempfile.mkdtemp())')" python server.py --no-browser --port 8131` (Git Bash; run it in the background). Use a new port number each time you want empty localStorage.

  Open http://localhost:8131 and check each of these:
  - **First visit:** `#/` changes to `#/start` and the three doors show.
  - **Some Python:**
    - wrong and right answers show the red or green state with the explanation;
    - 1–9 picks an answer and Enter continues;
    - answering 2 Python questions wrong shows the suggestion screen;
    - "Continue anyway" moves on to Big-O questions;
    - missing two topics ends the check;
    - the result screen lists placed-out topics, and "Start here" opens the start topic's first drill.
  - **Done DSA:** one question per topic, and no early stop. Start a fresh workspace for this.
  - **New to programming:** the interim page shows the skills and three course links. The links open outside Trace (a new browser tab; the system browser in the desktop app). "Take the ready check" starts the Python questions.
  - **Skip:** goes straight home, and home stays home after a reload.
  - **Stop here** on the first question places nothing, and the start is Big-O.

- [ ] **Step 9: Manual: existing learner.** Stop the server and restart it on your normal workspace (`python server.py --no-browser --port 8132`). That workspace already has solved problems and no placement. Opening `#/` must show home, not `#/start`.

- [ ] **Step 10: Manual: missing file.**
  1. Rename `course/starting_check.py` to `course/starting_check.off`.
  2. Open `#/start`: it says "The starting check isn't available" with a "Go to the topics" button, and home still loads.
  3. Rename the file back.

- [ ] **Step 11: Commit**

```bash
git add web/start.js web/index.html web/app.js web/app.css
git commit -m "Where are you starting? screen and adaptive check" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 5: Home and topic pages: Today card and placed-out topics

**Files:**
- Modify: `web/app.js` (`placedOut`, `nextUp`, `viewHome`, `viewTopic`)
- Modify: `web/app.css`

**Interfaces:**
- Consumes: `progress.placement` (Task 2); `firstVisit` (Task 4).
- Produces: `placedOut(topic) -> boolean` in `app.js`.

- [ ] **Step 1: Helper.** In `web/app.js`, directly after the `firstVisit` function from Task 4, add:

```js
  const placedOut = (topic) => (S.progress.placement?.placed_out || []).includes(topic.id);
```

- [ ] **Step 2: `nextUp()` skips placed-out topics.** Replace

```js
  function nextUp() {
    for (const topic of S.topics) {
```

  with

```js
  function nextUp() {
    for (const topic of S.topics) {
      if (placedOut(topic)) continue;
```

- [ ] **Step 3: The Today card.** In `viewHome()`, replace the whole `hero-actions` block:

```js
      h("div", { class: "hero-actions" },
        up ? h("a", { class: "btn primary", href: up.kind === "drill" ? `#/d/${up.dt.id}/${up.drill.id}` : up.kind === "walkthrough" ? `#/w/${up.topic.id}` : `#/p/${up.name}` },
          done || up.kind !== "drill" ? "Continue" : "Start", h("span", { style: "opacity:.7;font-weight:400" },
            up.kind === "drill" ? `${topicTitle(up.topic)}: intuition`
              : up.kind === "walkthrough" ? `${topicTitle(up.topic)}: read the code` : `${topicTitle(up.topic)}: ${S.problems[up.name].title}`)) : null,
        h("span", { class: "hero-stat" }, `${done} of ${total} exercises solved`)),
```

  with

```js
      h("section", { class: "today", "aria-label": "Today" },
        h("p", { class: "today-label" }, "Today"),
        up ? h("a", { class: "btn primary", href: up.kind === "drill" ? `#/d/${up.dt.id}/${up.drill.id}` : up.kind === "walkthrough" ? `#/w/${up.topic.id}` : `#/p/${up.name}` },
          done || up.kind !== "drill" ? "Continue" : "Start", h("span", { style: "opacity:.7;font-weight:400" },
            up.kind === "drill" ? `${topicTitle(up.topic)}: intuition`
              : up.kind === "walkthrough" ? `${topicTitle(up.topic)}: read the code` : `${topicTitle(up.topic)}: ${S.problems[up.name].title}`)) : null,
        h("span", { class: "hero-stat" }, `${done} of ${total} exercises solved`),
        S.progress.placement ? null : h("a", { class: "link", href: "#/start" }, "Take the starting check")),
```

- [ ] **Step 4: Placed-out tag on topic rows.** In `viewHome()`, replace

```js
            h("span", { class: "name" }, topicTitle(topic),
```

  with

```js
            h("span", { class: "name" }, topicTitle(topic), placedOut(topic) ? h("span", { class: "badge placed" }, "Placed out") : null,
```

- [ ] **Step 5: Retake link.** In `viewHome()`, replace

```js
      h("p", { style: "margin-top:48px" }, h("button", { class: "link", type: "button", onclick: resetAll }, "Reset all progress"))));
```

  with

```js
      h("p", { class: "home-foot" },
        S.progress.placement ? h("a", { class: "link", href: "#/start" }, "Retake the starting check") : null,
        h("button", { class: "link", type: "button", onclick: resetAll }, "Reset all progress"))));
```

- [ ] **Step 6: Topic-page note.** In `viewTopic()`, replace

```js
      h("div", { class: "topic-top" }, h("span", { class: "num" }, pad2(topic.n)), h("h1", {}, topicTitle(topic))),
```

  with

```js
      h("div", { class: "topic-top" }, h("span", { class: "num" }, pad2(topic.n)), h("h1", {}, topicTitle(topic))),
      placedOut(topic) ? h("p", { class: "placed-note" }, "You placed out of this. Everything stays open.") : null,
```

- [ ] **Step 7: Styles.** Append to `web/app.css`:

```css
/* ── Home: Today card, placed-out topics ────────────── */
.today { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-top: 24px; padding: 18px 20px; background: var(--fill); border-radius: var(--radius); }
.today-label { margin: 0; flex-basis: 100%; font-size: 12.5px; font-weight: 600; color: var(--ink-3); }
.badge.placed { color: var(--accent); background: var(--accent-soft); margin-left: 8px; vertical-align: 2px; }
.placed-note { margin: 14px 0 0; padding: 10px 14px; border-radius: var(--radius); background: var(--accent-soft); color: var(--accent); font-size: 15px; }
.home-foot { margin-top: 48px; display: flex; gap: 24px; flex-wrap: wrap; align-items: center; }
```

- [ ] **Step 8: Syntax check** with `node --check web/app.js`.

- [ ] **Step 9: Manual.** On a fresh workspace and port (as in Task 4, Step 8), check:
  - "Done DSA" with Big-O and toolkit answered right: home shows "Placed out" on topics 01 and 02, and the Today button points at topic 03's first drill.
  - Topic 01's page shows the note, and its ladder still opens.
  - The footer shows "Retake the starting check". Retaking with everything wrong removes the tags.
  - On your normal workspace (progress, no placement), the Today card shows "Take the starting check".
  - Light and dark mode, and a 390px-wide window.

- [ ] **Step 10: Commit**

```bash
git add web/app.js web/app.css
git commit -m "Home: Today card and placed-out topics" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 6: "How to work a problem" card

**Files:**
- Modify: `web/start.js` (add `T.howToCard`)
- Modify: `web/app.js` (`viewProblem`)
- Modify: `web/app.css`

**Interfaces:**
- Produces: `T.howToCard({onClose?}) -> HTMLElement`. Phase 3's "I'm stuck" panel reuses it.

- [ ] **Step 1: The card.** In `web/start.js`, add this just before the final `})();`:

```js
  // The four stages Trace uses everywhere. Shown on your first problem; "I'm stuck" (Phase 3) reuses it.
  const HOW = [
    ["Understand.", "Work the example by hand, then make up a smaller input and solve that too."],
    ["Plan.", "Say the brute force first, then look for the work it repeats."],
    ["Code.", "Write the slow version and get one test passing, then change one thing at a time."],
    ["Check.", "Open the first failing test, run your function on it with Try a call, and find where it differs from your plan."],
  ];
  T.howToCard = ({ onClose } = {}) => h("section", { class: "howto", "aria-label": "How to work a problem" },
    h("div", { class: "howto-head" }, h("h4", {}, "How to work a problem"),
      onClose ? h("button", { class: "btn ghost small", type: "button", onclick: onClose }, "Got it") : null),
    h("ol", {}, HOW.map(([stage, text]) => h("li", {}, h("strong", {}, stage), " ", text))));
```

- [ ] **Step 2: Show it on the first problem.** In `viewProblem()`, directly after

```js
    let showHint = false, solution = null, solutionShown = false, tab = "problem";
```

  add

```js
    let showHowTo = !local.get("trace.howtoSeen", false);
```

  Then in `renderLeft()`, in the `if (tab === "problem")` branch, replace

```js
            p.reported && p.reported.length ? h("span", { class: "badge reported", title: p.reported_note }, `Often reported: ${p.reported.join(", ")}`) : null),
          h("div", { class: "body-text" }, renderStatement(p.statement)));
```

  with

```js
            p.reported && p.reported.length ? h("span", { class: "badge reported", title: p.reported_note }, `Often reported: ${p.reported.join(", ")}`) : null),
          showHowTo
            ? T.howToCard({ onClose: () => { showHowTo = false; local.set("trace.howtoSeen", true); renderLeft(); } })
            : h("button", { class: "link howto-link", type: "button", onclick: () => { showHowTo = true; renderLeft(); } }, "How to work a problem"),
          h("div", { class: "body-text" }, renderStatement(p.statement)));
```

- [ ] **Step 3: Styles.** Append to `web/app.css`:

```css
/* ── How to work a problem ───────────────────────────── */
.howto { margin: 16px 0 0; padding: 14px 16px; background: var(--accent-soft); border-radius: var(--radius); }
.howto-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.howto h4 { margin: 0; font-size: 13px; font-weight: 600; color: var(--accent); }
.howto ol { margin: 8px 0 0; padding-left: 20px; color: var(--ink-2); font-size: 14.5px; }
.howto li { margin: 3px 0; }
.howto-link { display: inline-block; margin-top: 12px; font-size: 13.5px; }
```

- [ ] **Step 4: Syntax check** with `node --check web/start.js && node --check web/app.js`.

- [ ] **Step 5: Manual.** On a fresh port:
  - The first problem you open shows the card above the statement.
  - "Got it" hides it, and other problems then show only the "How to work a problem" link.
  - The link reopens the card.
  - It reads well in dark mode and in a narrow left pane.

- [ ] **Step 6: Commit**

```bash
git add web/start.js web/app.js web/app.css
git commit -m "How to work a problem card on the first problem" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 7: Spot the pattern only mixes reached topics

**Files:**
- Modify: `web/app.js` (`T.reachedTopics`, the home Review row, a `viewDrill` guard)
- Modify: `web/topics/review.js`
- Modify: `web/app.css`

**Interfaces:**
- Consumes: `placedOut`'s data (`progress.placement.placed_out`), `drillTopic`, `wtGot`, `pstate` (existing in `app.js`).
- Produces:
  - `T.reachedTopics() -> Set<topic id>`: a topic counts if it's placed out, any of its drills has been run, its walkthrough has been started, or any of its problems has a passing test.
  - `T.spotStatus() -> {ready: boolean, have: number, need: 4}`.

- [ ] **Step 1: `T.reachedTopics`.** In `web/app.js`, directly after the `placedOut` line from Task 5, add:

```js
  T.reachedTopics = () => {
    const out = new Set(S.progress.placement?.placed_out || []);
    for (const topic of S.topics) {
      const dt = drillTopic(topic);
      if ((dt && dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0)) || wtGot(topic) > 0
          || topic.items.some((n) => (pstate(n).passed || 0) > 0)) out.add(topic.id);
    }
    return out;
  };
```

- [ ] **Step 2: Filter the drill.** In `web/topics/review.js`:
  - Directly after `const ALL = Object.keys(P);`, add:

```js
  const TOPIC_OF = {
    hash: "04_hashing", two: "06_two_pointers", window: "07_sliding_window", prefix: "08_prefix_sums",
    bs: "09_binary_search", bsAns: "09_binary_search", sort: "10_sorting_and_intervals", greedy: "11_greedy",
    stack: "12_stacks", stackPlain: "12_stacks", deque: "13_queues_and_deques", fastslow: "14_linked_lists",
    heap: "17_heaps", trie: "18_tries", bfs: "19_graph_traversal", dfs: "19_graph_traversal",
    topo: "20_topological_sort_and_union_find", uf: "20_topological_sort_and_union_find",
    dijkstra: "21_weighted_graphs", back: "22_backtracking", dp: "23_dynamic_programming_1d", bits: "25_bit_tricks",
  };
  const NEED = 4;   // pattern topics: enough for a right answer and three wrong ones you've met
  const reachedKeys = () => {
    const seen = T.reachedTopics ? T.reachedTopics() : null;
    return seen ? ALL.filter((k) => seen.has(TOPIC_OF[k])) : ALL;
  };
  T.spotStatus = () => {
    const have = new Set(reachedKeys().map((k) => TOPIC_OF[k])).size;
    return { ready: have >= NEED, have: Math.min(have, NEED), need: NEED };
  };
```

  - Replace `signals: "Use this after a few topics are solid, and come back to it often. It mixes everything.",` with `signals: "It mixes the pattern topics you've started, so it grows as you go. Come back to it often.",`.
  - In `play(ctx)`, replace

```js
          const qs = T.sample(Q, 8);
```

    with

```js
          const keys = reachedKeys();
          const qs = T.sample(Q.filter(([, ans]) => keys.includes(ans)), 8);
```

    and replace

```js
            const opts = T.shuffle([ans, ...T.sample(ALL.filter((k) => k !== ans && P[k] !== P[ans]), 3)]);
```

    with

```js
            const opts = T.shuffle([ans, ...T.sample(keys.filter((k) => k !== ans && P[k] !== P[ans]), 3)]);
```

- [ ] **Step 3: The home Review row.** In `viewHome()`, directly after `const review = T.topics.find((d) => d.n === 99);`, add `const spot = review && T.spotStatus ? T.spotStatus() : null;`. Then replace the whole `review ? [ … ] : null,` block:

```js
      review ? [
        h("h2", { class: "section-title" }, "Review"),
        h("div", { class: "topic-list" }, h("a", { class: "topic-row", href: `#/d/${review.id}/${review.drills[0].id}` },
          h("span", { class: "num" }, "★"),
          h("span", { class: "name" }, review.title, h("span", { class: "sub" }, "Read a problem, name the technique. Mixes every topic.")),
          h("span", { class: "ladder-bar" }, T.pips(T.DrillProgress.rec(review, review.drills[0]).clean)))),
      ] : null,
```

  with

```js
      review ? [
        h("h2", { class: "section-title" }, "Review"),
        h("div", { class: "topic-list" }, spot && !spot.ready
          ? h("div", { class: "topic-row disabled" },
            h("span", { class: "num" }, "★"),
            h("span", { class: "name" }, review.title, h("span", { class: "sub" }, `Opens after four pattern topics (${spot.have} of ${spot.need}).`)),
            h("span"))
          : h("a", { class: "topic-row", href: `#/d/${review.id}/${review.drills[0].id}` },
            h("span", { class: "num" }, "★"),
            h("span", { class: "name" }, review.title, h("span", { class: "sub" }, "Read a problem, name the technique. Mixes the topics you've started.")),
            h("span", { class: "ladder-bar" }, T.pips(T.DrillProgress.rec(review, review.drills[0]).clean)))),
      ] : null,
```

- [ ] **Step 4: Guard the drill URL.** In `viewDrill()`, directly after the `crumbs(...)` line, add:

```js
    if (dt.n === 99 && T.spotStatus && !T.spotStatus().ready) {
      app.replaceChildren(h("div", { class: "page" }, h("h1", {}, dt.title),
        h("p", { class: "lede" }, `This mixes the techniques you've started, so it opens after four pattern topics. You've started ${T.spotStatus().have} so far.`),
        h("p", { style: "margin-top:24px" }, h("a", { class: "btn", href: "#/" }, "Back to the topics"))));
      return;
    }
```

- [ ] **Step 5: Styles.** Append to `web/app.css`:

```css
.topic-row.disabled { cursor: default; color: var(--ink-3); }
.topic-row.disabled:hover { background: none; }
```

- [ ] **Step 6: Syntax check** with `node --check web/app.js && node --check web/topics/review.js`.

- [ ] **Step 7: Manual: Spot the pattern gate.** On a fresh workspace and port:
  - Home's Review row reads "Opens after four pattern topics (0 of 4)" and isn't a link.
  - Opening `#/d/spot-pattern/spot` directly, or "Name it" from Ctrl+K, shows the explanation.
  - Back home, the row's pips still show no runs.
  - Now run one drill each in Hashing, Two pointers, Sliding window and Prefix sums. The row turns into a link, and every question and option in the drill is one of those four patterns.
  - On a "Done DSA" placement with everything right, the drill is open right away.

- [ ] **Step 8: Commit**

```bash
git add web/app.js web/topics/review.js web/app.css
git commit -m "Spot the pattern mixes only the topics you've reached" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 8: README and full verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README.** In `README.md`, after the paragraph that ends `plans (Blind 75, NeetCode 150, Beyond NeetCode) cut across the topics.`, add a blank line and:

```markdown
The first time you open Trace, it asks where you're starting: new to programming, some Python, or
DSA before. A short check (28 questions at most) puts you at your first gap. Topics you place out
of stay open, and you can retake the check from the home page.
```

- [ ] **Step 2: Unit tests.** Run `python -m unittest discover -s tests -v`. Expected: all pass.

- [ ] **Step 3: Self-check.** Run `python server.py --check starting 01_big 02_python sliding`. Expected: every line `ok`, ending with `All good.`

- [ ] **Step 4: Syntax.** Run `node --check web/start.js && node --check web/app.js && node --check web/topics/review.js && node --check web/topics/foundations.js`.

- [ ] **Step 5: End-to-end run-through.** Use a fresh workspace and port. Go through each door once, then on the resulting state check:
  - the Today card, placed-out tags, the topic-page note and the retake link;
  - the how-to card on the first problem;
  - the Spot the pattern gate, then the drill opening;
  - reset all progress, then a reload, which goes back to "Where are you starting?";
  - light and dark mode, and a 390px-wide window.

  If the desktop build is set up, run `python desktop/app.py` once and check that the interim page's course links open in the system browser.

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "README: the starting check" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
