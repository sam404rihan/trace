# "Read the code" step (pilot: sliding window)

**Status:** approved in conversation 2026-10-15. Built after the calm restyle, in its style.

## Problem

The ladder goes from visual drills (no code) straight to writing code (Snippet). Learners who
understand patterns by reading code have no step where they see the pattern's code built up
and explained piece by piece, and no bridge showing that harder problems reuse the same
skeleton.

## What the learner gets

A new rung, **Read the code**, between *Build the intuition* and *Snippet* on the topic page.
It opens a walkthrough at `#/w/<topic-id>`, one screen per layer:

1. **Layers.** Each layer adds one idea to the code. The screen shows a progress bar
   ("Layer i of n"), the title, a short "why" paragraph, and the code so far with the new lines
   highlighted and marked `+`.
2. **Run.** A Run button runs the layer's code (a complete program with a small example and
   prints) in the existing sandbox (`/api/run`) and shows the output.
3. **Check.** One multiple-choice question about that layer. Picking an option reveals the
   explanation (green if right, red if wrong, with the reason). Continue unlocks after any
   answer, right or wrong, like a drill. Back returns to the previous layer.
4. **Reuse.** The final screen(s) build a harder problem on the same skeleton. Changed lines
   are highlighted by role (e.g. *state*, *valid*, *answer*) with a small legend, and the screen
   links to that problem. It also has a check.

Sliding-window content:
- Layer 1, the loop: `right` walks the array, `left` stays 0, the window only grows.
- Layer 2, window state: a `counts` dict of what's inside. Check: why counts and not
  `set(a[left:right+1])`?
- Layer 3, shrink while invalid. Check: what breaks if `while` becomes `if`?
- Layer 4, record the answer after shrinking. Check: why record after the `while`?
- Reuse, Minimum window substring: shortest window, so shrink *while valid* and record inside
  the loop. Check about that flip.

The rung does not lock Snippet (drills don't lock anything either). It counts as done when
every screen has been answered.

**Dimmed skeleton.** On the Solution tab of sliding-window problems that use the
variable-size window, the skeleton lines are dimmed so the problem-specific lines stand out.

## Content format

`course/<stage>/<NN_topic>/walkthrough.py`, plain Python data, loaded like problem files:

```python
"""Build the sliding window, one layer at a time."""     # docstring = walkthrough title

LAYERS = [
    {
        "title": "The loop",
        "why": "Markdown text (same subset as lessons).",
        "code": '''...complete runnable program...''',
        "check": {
            "question": "What is the window after the last step?",
            "options": ["...", "...", "..."],
            "answer": 1,                    # index into options
            "explain": "Why the answer is right.",
        },
    },
    # ...
    {
        "title": "Same skeleton: Minimum window substring",
        "reuse": "min_window",              # problem name; the screen links to it
        "roles": {"state": "What the window tracks", "valid": "When to shrink", "answer": "Where the answer is recorded"},
        "why": "...",
        "code": '''... need[ch] -= 1  #@state ...''',
        "check": {...},
    },
]
```

**Line markers.** A trailing `#@name` comment tags a line (`x = 1  # note #@state`). The
server strips markers before sending code and returns them as line lists. Used for roles in
reuse layers and `#@skeleton` in solution files.

## Server (`server.py`)

- `parse_walkthrough(path)`: loads the module, validates it (every layer has title, why, code
  and a check whose `answer` indexes `options`; reuse roles used in code exist in `roles`),
  strips markers, and returns
  `{"title", "layers": [{"title", "why", "code", "added": [line numbers new vs the previous
  layer, via difflib], "marks": {role: [line numbers]}, "roles", "reuse", "check"}]}`.
  For layer 1 every line is "added". For reuse layers, `added` is empty and `marks` drives the
  highlighting.
- The course scan treats `walkthrough.py` like `lesson.py` (not a problem). Topics get
  `has_walkthrough` and `walkthrough_layers` (count).
- `GET /api/walkthrough?topic=<id>` returns the parsed walkthrough.
- Progress: `progress.json` gains `"walkthroughs": {topic_id: layers_answered}`.
  `POST /api/walkthrough-progress {"topic", "layers"}` stores the max. `/api/reset-progress`
  clears it too.
- `GET /api/solution` strips `#@` markers and adds `"skeleton": [line numbers]`.
- `--check` also runs every walkthrough layer's code in the sandbox and fails on a non-zero
  exit, and fails on any validation error.

## Frontend

- New `web/walkthrough.js` (keeps `app.js` from growing) exposing `T.mountWalkthrough(container,
  topic, data, {onProgress})`. `app.js` adds the `#/w/<id>` route, the rung, and its done state.
- Topic page `RUNGS` gains "Read the code" at index 1. It's done when
  `progress.walkthroughs[id] >= walkthrough_layers`.
- `nextUp()`: after a topic's drills have been started, if the topic has an unfinished
  walkthrough and no solved problems, point to the walkthrough.
- The Solution tab renders lines in `skeleton` with a `.dim` class.
- Styling follows the calm restyle: filled code block, accent `+` lines, role colours for reuse
  marks, filled answer choices with green/red feedback, a 4px progress bar.

## Tests

- `tests/test_walkthrough.py` (stdlib `unittest`): marker stripping, `added` diff lines,
  validation errors, parsing the real sliding-window walkthrough, skeleton extraction from a
  solution.
- `python server.py --check sliding` passes, including walkthrough layers.
- Manual run-through in the app: every layer, run, right and wrong answers, back, progress
  persisting after reload, the topic rung turning done, the dimmed solution.

## Out of scope

- Walkthroughs for topics other than sliding window (follows after the pilot is judged).
- Line-by-line execution stepper; typing layers back in; spaced review.
