# Trace

Learn data structures and algorithms in two passes: first in your head, then
in code. Every topic is a ladder:

| Rung | What you do |
|---|---|
| 0 Intuition | Short visual drills. You run the algorithm by hand, one decision at a time, and a wrong call tells you *why* it's wrong. |
| 1 Snippet | Write the core move in 2–5 lines (one pointer step, one relax, one bracket). |
| 2 Guided | One problem in three steps: make it work, handle the edges, make it fast. The last step has a big input that a brute-force answer can't finish in time. |
| 3 Problems | On your own, easy to hard, with hints and a reference solution. |
| 4 Build | A small real program that uses the idea: a rate limiter, an LRU cache, a route planner, a sudoku solver, a line diff… |

The next rung unlocks when you pass the current one ("Open anyway" if you want to skip).
34 topics in 6 stages, 383 coding exercises and 71 drills, with at least two hard problems in
every topic. Stage 6 (specialist topics) covers number theory, computational geometry, binary
lifting and rerooting, network flow and matching, and digit DP with monotonic-queue DP. Study
plans (Blind 75, NeetCode 150, Beyond NeetCode) cut across the topics.

## Start it

### The desktop app (no Docker)

```
python desktop/build.py              # builds dist/Trace/Trace.exe (first time: a few minutes)
python desktop/build.py --shortcut   # ...and adds Trace to the Desktop and Start menu
```

Then open `dist/Trace/Trace.exe`. It's a normal window (Edge WebView2, already on Windows 10/11)
with everything bundled: the course, the fonts, the editor, and its own Python 3.14 that your
code runs on. It works offline and needs nothing else installed. To share it, zip the whole
`dist/Trace` folder.

The build makes a private environment in `.build-venv/` (PyInstaller, pywebview, Pillow) and
downloads the official embeddable Python into `runtime/python/` if it isn't there.

To run the desktop window from source instead: `pip install pywebview`, then `python desktop/app.py`.

### In the browser

```
npm start          (or: python server.py)
```

Your browser opens <http://localhost:8000>. Use `python server.py --port 9000` if 8000 is taken.
You need Python 3.10+. Code runs on `runtime/python` (3.14) when it's present, otherwise on
the Python that started the server.

Docker is optional: `python server.py --sandbox docker` runs every test in a throwaway
container instead, and `docker compose up -d` runs the server itself in Docker.

### Desktop shortcuts

| Keys | Does |
|---|---|
| Ctrl+K (or Ctrl+P) | Go to anything: problems, topics, plans, drills. Type part of a name or its initials ("lis") |
| Ctrl+B | Show or hide the sidebar |
| Alt+← / Alt+→ | Previous / next problem in the workspace |

## Using the workspace

- **No imports needed.** Like LeetCode, the usual toolkit is preloaded: `deque`, `Counter`,
  `defaultdict`, `OrderedDict`, `heappush`/`heappop`/`heapify`, max-heaps (`heappush_max`,
  `heappop_max`, `heapify_max`, `heapreplace_max`, `heappushpop_max`, or a `MaxHeap` object),
  `bisect_left`/`bisect_right`,
  `lru_cache`/`cache`, `reduce`, `accumulate`, `permutations`/`combinations`/`product`,
  `inf`, `gcd`, `sqrt`, `isqrt`, `comb`, `List`/`Optional`/`Dict`…, `ListNode`/`TreeNode`,
  plus the modules `math`, `collections`, `heapq`, `bisect`, `itertools`, `functools`,
  `re`, `random`, `string`. The full list is in `runner/prelude.py`. Your own definitions always win.
- **Ctrl+Enter** runs the tests, and **Ctrl+S** saves (it autosaves anyway).
- **Try a call** runs one expression of your own, e.g. `two_sum([1, 4, 6], 10)`.
- A failing test opens automatically, and the line that raised an error is highlighted.
- Guided problems run only the steps you've reached. Passing a step opens the next one.
- The **Solution** tab holds a commented reference solution.

Drills: keys `1`–`9` answer, `H` shows the answer (counts as a slip), `N` gives a new
example, and `Enter` goes to the next one. Three clean runs make a drill solid.

## The sandbox

Every Run starts a fresh, separate Python process (two are kept warm, so a Run takes a
fraction of a second). On Windows it sits in a Job Object limited to 512 MB of memory that
can't start other processes, and it's killed if Trace exits. Each test gets 2 seconds.
The server listens on 127.0.0.1 only. With `--sandbox docker`, runs use a container with no
network, 256 MB, 1 CPU and a read-only filesystem.

## Your data

Your code and solved problems are saved in `workspace/` when you run from source, and in
`%LOCALAPPDATA%\Trace\workspace` for the desktop app (delete it to start over). Set
`TRACE_WORKSPACE` to use another folder.
Drill progress is kept in your browser. "Reset all progress" on the home page clears
both, but keeps your code.

## Adding exercises

Put a `.py` file in a topic folder under `course/`. The function (or class) name must
match the file name, and the docstring's first line is `Title   [snippet|guided|easy|medium|hard|build]`.

- Plain tests: `TESTS = [((args...), expected), ...]`
- Guided: `STEPS = [{"title", "text", "hint", "tests": [...]}, ...]`
- Classes: `CLASS = "Name"` with tests like `([("Name", 2), ("put", 1, 1), ("get", 1)], [None, None, 1])`
- Optional: `PREPARE(*args)`, `FINISH(value)`, `CHECK(got, expected[, args])` for answers with many valid forms.

Put a reference solution in `solutions/<name>.py`, then verify every solution and starter in the sandbox:

```
python server.py --check            (or --check two_pointers lru_cache to filter)
```

## Files

```
server.py        local server: course loader, progress, one sandboxed process per run
runner/          the judge and the prelude (plus a Dockerfile for --sandbox docker)
runtime/python/  the embeddable Python 3.14 your code runs on (downloaded by desktop/build.py; not in git)
desktop/         app.py (the window) and build.py (makes Trace.exe)
course/          <stage>/<NN_topic>/ lesson.py (cheat sheet) + exercises
solutions/       reference solutions
web/             the app: index.html, app.css, app.js (pages + IDE), drill.js, core.js, topics/ (drills)
helpers.py       ListNode, TreeNode, build_list, build_tree, ... (importable in your code)
structures/, algorithms/   full implementations, also importable
legacy_ide/      the previous version's UI and server, kept for reference
```

## License

MIT, see [LICENSE](LICENSE).

Bundled third-party files keep their own licenses:

- [CodeMirror 5](https://codemirror.net/5/) (`web/vendor/codemirror/`): MIT, Copyright (C) 2017 by Marijn Haverbeke and others
- [IBM Plex Mono](https://github.com/IBM/plex) (`web/vendor/fonts/`): SIL Open Font License 1.1, Copyright © 2017 IBM Corp.
- [Schibsted Grotesk](https://github.com/schibsted/schibsted-grotesk) (`web/vendor/fonts/`): SIL Open Font License 1.1,
  Copyright 2023 The Schibsted Grotesk Project Authors
