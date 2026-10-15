# Calm restyle + "Read the code" step Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle Trace to the approved "calm and clean" look, then add a "Read the code" rung that builds the sliding-window pattern up in layers (read, run, check) and ends with a reuse walkthrough, plus dimmed skeleton lines on solution tabs.

**Architecture:** The restyle is token and component CSS in `web/app.css`. The Read step adds a course content file (`walkthrough.py`), parsing, validation and a progress endpoint in `server.py`, a self-contained view module `web/walkthrough.js`, and small hooks in `web/app.js` (route, rung, next-up, solution dimming).

**Tech Stack:** Python 3.10+ stdlib server (`http.server`, `ast`, `difflib`), vanilla JS (no build step), CSS custom properties, stdlib `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-15-calm-restyle-design.md`, `docs/superpowers/specs/2026-10-15-read-the-code-step-design.md`

## Global Constraints

- No new dependencies: no pip packages, no npm packages, no new fonts. Fonts stay Schibsted Grotesk + IBM Plex Mono from `web/vendor/fonts`.
- The app must keep working offline (desktop build).
- Every colour token added must have a dark value in both dark blocks (`@media (prefers-color-scheme: dark) :root:not([data-theme="light"])` and `:root[data-theme="dark"]`).
- Accent: light `#4f5fe0`, dark `#8e9bff`. Fill: light `#f6f7fb`, dark `#1b1c22`. Radius 12px; buttons are pills.
- Green only for passed/correct, orange-red only for failed/wrong.
- Line marker syntax: a trailing `#@name` comment.
- Match surrounding code style: dense, comment-light, `h(...)` DOM helpers in JS.

## Review Focus

1. A broken `walkthrough.py` (bad answer index, typo in a marker) must not take down the whole course: the topic just has no walkthrough, the server logs why, and `--check` fails loudly. Test: `test_broken_walkthrough_is_skipped_not_fatal`.
2. Progress posts with a bogus topic or a layer count out of range must be rejected, and a smaller count must never lower stored progress. Test: `test_walkthrough_progress_is_max_and_validated`.
3. Solutions without markers must come back byte-for-byte unchanged, with an empty `skeleton`. Test: `test_unmarked_code_is_unchanged`.
4. A `#@` that isn't at the end of a line (e.g. inside a string) must not be treated as a marker. Test: `test_marker_only_at_line_end`.
5. Running a layer while the sandbox is down shows the sandbox message, not a crash. Covered by reusing the `docker_error` path from the lesson Run button (manual check in Task 6).

---

### Task 1: Calm restyle (CSS)

**Files:**
- Modify: `web/app.css` (tokens at the top, then component rules throughout)

- [ ] **Step 1: Tokens.** In `:root` set `--accent: #4f5fe0; --accent-soft: #eceffd;`, add `--accent-ink: #ffffff; --fill: #f6f7fb; --fill-2: #eceef5;` and set `--radius: 12px;`. In both dark blocks add `--accent: #8e9bff; --accent-soft: #1f2445; --accent-ink: #0d0f1f; --fill: #1b1c22; --fill-2: #24262e;`.
- [ ] **Step 2: Type.** `body` font 15px/1.55. New rule: `.page, .drill-page, .wt-page { font-size: 16.5px; line-height: 1.6; }`. `.page h1` 40px / -0.03em. `.lede` 18.5px. `.section-title` 14px. `.prose` 17px/1.65 (with `.prose pre` 14px). `.statement` 15.5px. `.stat b` 26px.
- [ ] **Step 3: Buttons.** `.btn`: `border: 0; border-radius: 999px; background: var(--fill); height: 36px; padding: 0 18px;` hover `--fill-2`. `.btn.primary` and `.btn.run`: `background: var(--accent); color: var(--accent-ink);` hover `filter: brightness(1.06)`. Remove the dark `.btn.run` colour overrides (replaced by `--accent-ink`). `.btn.small` 30px / `0 12px`.
- [ ] **Step 4: Surfaces without borders.** Replace borders with fills on: `.topic-list` (no border-top), `.topic-row` (no border-bottom, `border-radius: var(--radius)`, hover `--fill`), `.facts`, `.item` (fill, hover fill-2, locked `opacity: .6`), `.chip-link`, `details.sheet` (fill; `.sheet .prose pre` uses `--bg`), `.prose pre`, `.callout`, `.reveal-box`, `.step` (current: `box-shadow: inset 0 0 0 1.5px var(--accent)`), `.step-pill` (fill; current: accent ring; locked opacity), `.drill-tab` (fill; selected accent), `.test` (no border), `.search-btn` (no border), `.code` (no border, fill).
- [ ] **Step 5: Accent for "where you are".** `.rung.current .rung-dot`, `.step.current .step-num`, `.tab[aria-selected]` underline and `.side-link[aria-current]` (`background: var(--accent-soft); color: var(--accent); box-shadow: none`) use the accent instead of ink.
- [ ] **Step 6: Drill console and choices.** `.board`: no border, `border-radius: 16px`. `.dconsole`: no border, `background: var(--fill); border-radius: 16px; margin-top: 8px`. `.opt`: `border: 0; border-radius: var(--radius); background: var(--fill); padding: 10px 16px;` hover `box-shadow: inset 0 0 0 1.5px var(--line-2)`; inside `.dconsole` `.opt` uses `--bg`. `.opt.primary` accent. `.opt.miss`: `background: var(--bad-soft); color: var(--bad); box-shadow: inset 0 0 0 1.5px var(--bad)`. Add `.opt.right` (ok-soft, ok, ok ring) and `.opt.wrong` (same as miss without animation).
- [ ] **Step 7: Shared progress bar.** Add `.progress { height: 4px; border-radius: 4px; background: var(--fill-2); overflow: hidden; } .progress i { display: block; height: 100%; width: calc(var(--p, 0) * 100%); background: var(--accent); border-radius: 4px; transition: width .25s ease; }` and include `.progress i` in the reduced-motion rule.
- [ ] **Step 8: Verify.** `python server.py --no-browser --port 8123` in the background; open home, a topic page, a drill (answer right and wrong), a problem (run failing and passing), solution tab, cheat sheet, sidebar; in light and dark (`theme-btn`), and at 390px width. Fix contrast or spacing issues found.
- [ ] **Step 9: Commit** `git add web/app.css && git commit -m "Restyle: calm and clean surfaces, type and accent"`

### Task 2: Line markers and diff helpers (server, TDD)

**Files:**
- Modify: `server.py` (Course section, after `parse_lesson`)
- Create: `tests/test_walkthrough.py`

**Interfaces:**
- Produces: `strip_markers(code: str) -> tuple[str, dict[str, list[int]]]` (1-based line numbers); `added_lines(before: str, after: str) -> list[int]` (1-based lines of `after`, blank lines excluded).

- [ ] **Step 1: Failing tests**

```python
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class StripMarkers(unittest.TestCase):
    def test_strips_and_reports(self):
        code, marks = server.strip_markers("a = 1  #@state\nb = 2  # note #@state\nc = 3\nd = 4 #@valid")
        self.assertEqual(code, "a = 1\nb = 2  # note\nc = 3\nd = 4")
        self.assertEqual(marks, {"state": [1, 2], "valid": [4]})

    def test_unmarked_code_is_unchanged(self):
        src = "def f(x):\n    return x  # plain comment\n"
        self.assertEqual(server.strip_markers(src), (src, {}))

    def test_marker_only_at_line_end(self):
        src = 's = "#@state inside"\n'
        self.assertEqual(server.strip_markers(src), (src, {}))


class AddedLines(unittest.TestCase):
    def test_new_and_changed_lines(self):
        self.assertEqual(server.added_lines("a\nb\nc", "a\nx\nb\n\nc\ny"), [2, 6])

    def test_first_layer_is_all_new(self):
        self.assertEqual(server.added_lines("", "a\n\nb"), [1, 3])
```

- [ ] **Step 2: Run** `python -m unittest discover -s tests -v` → fails with `AttributeError: module 'server' has no attribute 'strip_markers'`.
- [ ] **Step 3: Implement** (add `import difflib` and `import textwrap` to the imports):

```python
MARKER = re.compile(r"\s*#@([A-Za-z_][\w-]*)\s*$")


def strip_markers(code):
    """Remove trailing '#@name' line tags. Returns the clean code and {name: [line numbers]}."""
    lines, marks = [], {}
    for number, line in enumerate(code.split("\n"), 1):
        m = MARKER.search(line)
        if m:
            marks.setdefault(m.group(1), []).append(number)
            line = line[:m.start()]
        lines.append(line)
    return "\n".join(lines), marks


def added_lines(before, after):
    """Line numbers in `after` that are new or changed compared with `before` (blank lines ignored)."""
    new = after.split("\n")
    matcher = difflib.SequenceMatcher(a=before.split("\n") if before else [], b=new, autojunk=False)
    return [j + 1 for tag, _, _, j1, j2 in matcher.get_opcodes() if tag in ("insert", "replace")
            for j in range(j1, j2) if new[j].strip()]
```

- [ ] **Step 4: Run tests** → 5 pass.
- [ ] **Step 5: Commit** `git add server.py tests/test_walkthrough.py && git commit -m "Add line-marker and line-diff helpers"`

### Task 3: Walkthrough parsing, API, progress, solution skeleton (server, TDD)

**Files:**
- Modify: `server.py` (`parse_walkthrough`, `CourseCache._build`, `/api/course`, `/api/walkthrough`, `/api/walkthrough-progress`, `/api/reset-progress`, `/api/solution`, `load_progress`, `check`)
- Test: `tests/test_walkthrough.py`

**Interfaces:**
- Consumes: `strip_markers`, `added_lines` (Task 2), existing `load_module`.
- Produces: `parse_walkthrough(path) -> {"title": str, "layers": [{"title", "why", "code", "added": [int], "marks": {role: [int]}, "roles": {role: label}, "reuse": str|None, "check": {"question", "options", "answer", "explain"}}]}`; raises `ValueError` naming the file and layer. Topics gain `walkthrough` (internal), exposed as `has_walkthrough: bool`, `walkthrough_layers: int`. `progress["walkthroughs"]: {topic_id: int}`. `POST /api/walkthrough-progress {"topic": id, "layers": n}` → `{"progress": ...}`. `GET /api/solution` → `{"code", "skeleton": [int]}`. Helper `record_walkthrough(topic_id, layers, total) -> progress` raising `ValueError` on bad input.

- [ ] **Step 1: Failing tests** (append):

```python
GOOD = '''
"""Build it."""
LAYERS = [
    {"title": "One", "why": "w", "code": """
x = 1
print(x)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 1, "explain": "e"}},
    {"title": "Two", "why": "w", "code": """
x = 1
y = 2
print(x)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 0, "explain": "e"}},
    {"title": "Reuse", "why": "w", "reuse": "min_window", "roles": {"state": "S"}, "code": """
z = 3  #@state
print(z)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 0, "explain": "e"}},
]
'''


def write(tmp, source, name="walkthrough.py"):
    path = Path(tmp) / name
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseWalkthrough(unittest.TestCase):
    def test_parses_layers(self):
        with tempfile.TemporaryDirectory() as tmp:
            wt = server.parse_walkthrough(write(tmp, GOOD))
        self.assertEqual(wt["title"], "Build it.")
        one, two, reuse = wt["layers"]
        self.assertEqual(one["code"], "x = 1\nprint(x)")
        self.assertEqual(one["added"], [1, 2])
        self.assertEqual(two["added"], [2])
        self.assertEqual(reuse["added"], [])
        self.assertEqual(reuse["marks"], {"state": [1]})
        self.assertEqual(reuse["code"], "z = 3\nprint(z)")
        self.assertEqual(reuse["reuse"], "min_window")

    def test_bad_answer_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "layer 1"):
                server.parse_walkthrough(write(tmp, GOOD.replace('"answer": 1', '"answer": 5')))

    def test_unknown_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "valid"):
                server.parse_walkthrough(write(tmp, GOOD.replace("#@state", "#@valid")))

    def test_real_sliding_window(self):
        path = next(server.COURSE.glob("*/07_sliding_window/walkthrough.py"))
        wt = server.parse_walkthrough(path)
        self.assertGreaterEqual(len(wt["layers"]), 5)
        self.assertEqual(wt["layers"][-1]["reuse"], "min_window")
        self.assertEqual(set(wt["layers"][-1]["marks"]), {"state", "valid", "answer"})
        self.assertNotIn("#@", "".join(l["code"] for l in wt["layers"]))


class CourseIntegration(unittest.TestCase):
    def test_topic_exposes_walkthrough(self):
        topics, problems = server.load_course()
        topic = next(t for t in topics if t["id"] == "07_sliding_window")
        self.assertTrue(topic["walkthrough"])
        self.assertNotIn("walkthrough", topic["items"])

    def test_broken_walkthrough_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, GOOD.replace('"answer": 1', '"answer": 9'))
            self.assertIsNone(server.load_walkthrough_safely(path))


class Progress(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = server.PROGRESS_FILE, server.WORKSPACE
        server.WORKSPACE = Path(self.tmp.name)
        server.PROGRESS_FILE = server.WORKSPACE / "progress.json"

    def tearDown(self):
        server.PROGRESS_FILE, server.WORKSPACE = self.old
        self.tmp.cleanup()

    def test_walkthrough_progress_is_max_and_validated(self):
        self.assertEqual(server.record_walkthrough("t", 3, 5)["walkthroughs"], {"t": 3})
        self.assertEqual(server.record_walkthrough("t", 1, 5)["walkthroughs"], {"t": 3})
        for bad in (-1, 6, "2", True):
            with self.assertRaises(ValueError):
                server.record_walkthrough("t", bad, 5)


class SolutionSkeleton(unittest.TestCase):
    def test_marked_solution(self):
        code, marks = server.strip_markers((server.SOLUTIONS / "longest_k_distinct.py").read_text(encoding="utf-8"))
        self.assertTrue(marks.get("skeleton"))
        self.assertNotIn("#@", code)
```

- [ ] **Step 2: Run** → new tests fail (`parse_walkthrough` missing; file missing).
- [ ] **Step 3: Implement `parse_walkthrough` and `load_walkthrough_safely`:**

```python
def parse_walkthrough(path):
    """walkthrough.py: a docstring title and LAYERS, each building the topic's code one idea further."""
    module = load_module(path)
    layers = module.get("LAYERS")
    if not isinstance(layers, list) or not layers:
        raise ValueError(f"{path.name}: LAYERS must be a non-empty list")
    out, previous = [], ""
    for i, layer in enumerate(layers, 1):
        where = f"{path.name} layer {i}"
        missing = [k for k in ("title", "why", "code", "check") if not layer.get(k)]
        if missing:
            raise ValueError(f"{where}: missing {', '.join(missing)}")
        check, options = layer["check"], layer["check"].get("options") or []
        answer = check.get("answer")
        if not check.get("question") or not check.get("explain") or len(options) < 2 \
                or type(answer) is not int or not 0 <= answer < len(options):
            raise ValueError(f"{where}: check needs a question, 2+ options, an answer index into them, and an explanation")
        code, marks = strip_markers(textwrap.dedent(layer["code"]).strip("\n"))
        roles = layer.get("roles") or {}
        unknown = sorted(set(marks) - set(roles))
        if unknown:
            raise ValueError(f"{where}: marker(s) {', '.join(unknown)} not listed in roles")
        reuse = layer.get("reuse") or None
        out.append({"title": layer["title"], "why": textwrap.dedent(layer["why"]).strip(), "code": code,
                    "added": [] if reuse else added_lines(previous, code), "marks": marks, "roles": roles,
                    "reuse": reuse, "check": {k: check[k] for k in ("question", "options", "answer", "explain")}})
        if not reuse:
            previous = code
    title = (module.get("__doc__") or "").strip() or folder_label(path.parent.name)
    return {"title": title, "layers": out}


def load_walkthrough_safely(path):
    """A broken walkthrough hides itself (and says why) rather than taking the course down. --check fails on it."""
    try:
        return parse_walkthrough(path)
    except Exception as exc:  # noqa: BLE001 - course content, reported, never fatal
        sys.stderr.write(f"  walkthrough skipped: {exc}\n")
        return None
```

- [ ] **Step 4: Wire into the course.** In `CourseCache._build`: skip `walkthrough.py` in the problem glob (`if p.name in ("lesson.py", "walkthrough.py") or ...`), load it like the lesson via `self._cached(wt_path, sig.get(str(wt_path)), load_walkthrough_safely)` when present, and set `topic["walkthrough"] = wt`. In `/api/course`, exclude `lesson` and `walkthrough` from the topic dict and add `"has_walkthrough": bool(t["walkthrough"]), "walkthrough_layers": len(t["walkthrough"]["layers"]) if t["walkthrough"] else 0`. Add `GET /api/walkthrough?topic=` returning `topic["walkthrough"]` or 404 `"Unknown walkthrough"`.
- [ ] **Step 5: Progress.** `load_progress` gets `progress.setdefault("walkthroughs", {})`. Add:

```python
def record_walkthrough(topic_id, layers, total):
    if type(layers) is not int or not 0 <= layers <= total:
        raise ValueError("layers must be a whole number within the walkthrough")

    def change(progress):
        progress["walkthroughs"][topic_id] = max(progress["walkthroughs"].get(topic_id, 0), layers)
    return update_progress(change)
```

  `POST /api/walkthrough-progress`: find the topic with a walkthrough (else `fail("Unknown walkthrough")`), call `record_walkthrough(topic["id"], data.get("layers"), len(...))`, turning `ValueError` into `self.fail(str(exc))`. `/api/reset-progress` also sets `progress["walkthroughs"] = {}`.
- [ ] **Step 6: Solution skeleton.** `/api/solution` → `code, marks = strip_markers(text)`; return `{"code": code, "skeleton": marks.get("skeleton", [])}`.
- [ ] **Step 7: `--check`.** After the problem loop, for each `COURSE.glob("*/*/walkthrough.py")` matching `only` (by topic dir name): `parse_walkthrough` (fail on `ValueError`), fail if a `reuse` name isn't in `problems`, and `run_script(layer["code"])` each layer, failing on non-zero `exit_code` or `killed`. Print `ok  ` / `FAIL` lines like the problem loop.
- [ ] **Step 8: Content.** Create `course/2_core_patterns/07_sliding_window/walkthrough.py` (Task 4) before running the tests that read it; then mark solution skeletons (Task 4 step 2).
- [ ] **Step 9: Run tests** → all pass. Run `python server.py --check sliding` → all ok, including walkthrough layers.
- [ ] **Step 10: Commit** `git commit -m "Serve walkthroughs: parsing, validation, progress, solution skeleton"`

### Task 4: Sliding-window content

**Files:**
- Create: `course/2_core_patterns/07_sliding_window/walkthrough.py`
- Modify: sliding-window solutions that use the variable-size window (`longest_k_distinct`, `character_replacement`, `min_subarray_len`, `subarrays_k_distinct`, `min_window`, others after reading them): add `#@skeleton` to the `left = 0` line, the `for right ...` header, the `while ...:` header and `left += 1` lines, only where the line is pure skeleton.

- [ ] **Step 1: Write `walkthrough.py`** with five layers, all inside `def longest_k_distinct(s, k):` from layer 1 so indentation never changes between layers:
  1. *The loop*: `left = 0`, `for right in range(len(s))`, print the window; call on `"abcbbca", 2`. Check: what is the window after the last step? → the whole string.
  2. *Window state*: `counts` dict. Check: why counts and not `len(set(...))`? → O(1) per step.
  3. *Shrink while invalid*: `while len(counts) > k` with delete-at-zero. Check: `while` → `if`? → window can stay invalid (the final `a` needs four steps from the left).
  4. *Record the answer*: `left = best = 0`, `best = max(...)` after the `while`, `return best`, prints `5`. Check: why after the `while`? → before it the window may be invalid.
  5. *Reuse, Minimum window substring* (`reuse: "min_window"`, roles state/valid/answer) with `need`/`missing`, `while missing == 0`, recording inside the loop. Check: where do you record for "shortest"? → inside the `while`, before shrinking.
- [ ] **Step 2: Mark skeletons** in the solutions listed above.
- [ ] **Step 3:** `python server.py --check sliding` passes (solutions still pass with markers; layers run).
- [ ] **Step 4: Commit** `git commit -m "Sliding window: layered walkthrough and skeleton markers"`

### Task 5: Walkthrough view (`web/walkthrough.js`) and styles

**Files:**
- Create: `web/walkthrough.js`
- Modify: `web/index.html` (script tag after `drill.js`), `web/app.js` (export `T.renderMarkdown = renderMarkdown; T.inline = inline;`), `web/app.css` (walkthrough block)

**Interfaces:**
- Consumes: `/api/walkthrough` payload (Task 3), `T.h`, `T.renderMarkdown`, `T.inline`.
- Produces: `T.mountWalkthrough(container, topic, wt, { done, run, onAnswer, problemHref, topicHref }) -> { unmount }` where `run(code) -> Promise<{output, killed} | {docker_error}>`, `onAnswer(layersAnswered: number)`.

- [ ] **Step 1: Implement the module.** One screen per layer: `.progress` bar (`--p` = (i+1)/n), label (`Layer i of n`, or `Same skeleton` for reuse layers), `h1` title, `.prose.wt-why` from `T.renderMarkdown(layer.why)`, a legend of roles for reuse layers, `pre.wt-code` with one `span.ln` per line (`data-g="+"` and class `add` for added lines; class `r0..r3` by role index for marked lines), a Run button that calls `run(code)` and shows output in `pre.run-out`, then the check (`.wt-q` + `.opt` buttons via `T.inline`). Answering disables options, marks the pick `.right`/`.wrong` (and the correct one `.right`), shows `.wt-explain.ok|.bad` with "Right." / "Not quite." + explain, and calls `onAnswer(i + 1)`. Nav: Back (if i > 0) and Continue (enabled once answered or `i < done`); on the last layer Continue becomes "Back to the topic" (`topicHref`). Reuse layers show an "Open the problem" link (`problemHref(name)`). Keys: `1`–`9` answer, `Enter` continue, ignored inside inputs. Start at `min(done, n - 1)`.
- [ ] **Step 2: Styles** in `app.css`: `.wt-page` (max-width 760px, centered, padding 36px 24px 96px), `.wt-label` (accent, 13.5px, 600), `.wt-page h1` (30px), `.wt-code` (fill, radius 12, 14px/1.75 mono, `.ln::before { content: attr(data-g); width: 28px }`, `.add` accent-soft, `.r0..r3` using `--pa..--pd` soft fills and a 3px inset left bar), `.wt-legend`, `.wt-check`, `.wt-q` (18px, 600), `.wt-opts` (grid, gap 8px, full-width `.opt`), `.wt-explain.ok|.bad`, `.wt-nav`.
- [ ] **Step 3:** `node --check web/walkthrough.js && node --check web/app.js`.
- [ ] **Step 4: Commit** `git commit -m "Walkthrough view: layered code, run, check"`

### Task 6: App wiring and solution dimming

**Files:**
- Modify: `web/app.js`, `web/app.css`

- [ ] **Step 1: Route** `#/w/<topic-id>` → `viewWalkthrough(id)`: crumbs Topics › topic › Read the code; fetch `/api/walkthrough`; mount with `run: (code) => api("/api/run", { code })` (call `showDocker` on `docker_error`), `onAnswer` posting to `/api/walkthrough-progress` only when it raises progress, then updating `S.progress`.
- [ ] **Step 2: Topic page rung.** Insert `["Read the code", "The pattern's code, built up one piece at a time."]` at index 1 of `RUNGS`; `groups[1]` is `["walkthrough"]` when `topic.has_walkthrough`; `rungDone(1)` uses `wtDone(topic)`; render one `.item` row linking to `#/w/id` showing "`x` of `n` layers" and solved/partial state.
- [ ] **Step 3: Next up and home.** `nextUp()` returns `{ kind: "walkthrough", topic }` when drills are started, the walkthrough isn't done and nothing in the topic is solved. The home Continue button handles that kind (`#/w/id`, "`Topic`: read the code"). `ladderBar` adds one dot for the walkthrough.
- [ ] **Step 4: Dimmed skeleton.** Keep the `/api/solution` payload; render the solution as one `span` per line with `.dim` for skeleton lines and a one-line note above ("Dimmed lines are the pattern's skeleton. The rest is what this problem adds."). CSS: `.solution-box .dim { opacity: .45; }`.
- [ ] **Step 5: Verify in the app** (server on 8123): topic page shows the new rung; walkthrough: every layer, Run output, a right and a wrong answer, Back, reload keeps progress, last layer returns to topic and the rung shows done; home Continue points correctly; Reset all progress clears it; min_window solution shows dimmed lines; light/dark; 390px width; stop the sandbox scenario is covered by the shared `docker_error` path.
- [ ] **Step 6: Run** `python -m unittest discover -s tests -v` and `python server.py --check sliding`.
- [ ] **Step 7: Commit** `git commit -m "Wire the Read-the-code rung into topics, home and solutions"`
