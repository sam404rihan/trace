# Beginner path: start anywhere, keep what you learn

**Status:** draft for review, 2026-10-16. Built from the research gathered in conversation the same
day; every decision below cites its sources (links at the end).
**Scope:** four phases. Each ships on its own and gets its own implementation plan:

1. Starting check and first hour
2. Review queue
3. Help that teaches
4. Beginner content (Stage 1 walkthroughs, Stage 0 "Python from zero")

## Goal

Anyone who opens Trace, from someone who has never programmed to someone who has done DSA before,
should know where to start within a few minutes, get a real win in the first session, and still
remember week-one material a month later. The 34-topic ladder stays the core. This work adds a way
in (placement and a floor), a way back (reviews), and help that teaches instead of only revealing.

## Assumptions

- **Both kinds of beginner, in stages.** Phases 1–3 serve learners who can already write some
  Python. Phase 4 adds Stage 0 for people who can't. Until Phase 4 ships, the "new to programming"
  choice shows an interim page.
- Trace stays offline, single-user and Python-only.
- **Calm**, per the restyle spec: no streaks, badges or reminders. Progress is shown, not pushed.
- Content (check questions, walkthroughs, Stage 0 exercises) is written during each phase's plan,
  in the formats defined here.

## What a beginner meets today

- "Start" opens *Call the cost*, which asks whether a line is O(1), O(log n), O(n) or O(n log n).
  Big-O is taught in topic 02, after it. Seven of the nine toolkit problems already say
  "Aim for O(…)".
- Topic 01 is a toolkit reference for people who already code. Nothing checks or teaches what
  comes before it.
- No placement: experienced learners start at topic 01, and people who can't code have nowhere
  to start.
- 49 of 383 exercises are easy. *Read the code* exists only for sliding window, a Stage 2 topic.
- One hint per problem or step, then the full solution. Viewing the solution changes nothing.
- Nothing comes back. Drill progress lives in localStorage with no dates, so the three clean runs
  that make a drill solid can happen in one sitting. A problem solved once is done for good.
- *Spot the pattern* samples all 36 questions, so a learner three topics in mostly meets
  techniques they haven't learned.

## Principles from the research

1. **Start at the first gap; skip what you already know.** Math Academy places every student with
   an adaptive diagnostic. Khan Academy's course challenges move skill levels up or down. Guidance
   that experienced learners don't need slows them (expertise reversal effect). Mastery sequencing
   raised exam scores across 108 controlled studies, most for weaker students (Kulik et al. 1990).
2. **Soft locks, not hard ones.** The same review found that self-paced mastery programmes often
   lowered completion. "Open anyway" stays.
3. **A real success early.** Mastery experiences are the strongest source of self-efficacy
   (Bandura). Self-efficacy and a working mental model of the program both predicted success in
   intro programming (Wiedenbeck et al. 2004).
4. **Read and trace before writing.** Tracing and explaining scores accounted for 46% of the
   variance in code-writing scores (Lopez et al. 2008). Teach tracing, then syntax, then reading
   patterns, then writing with them (Xie et al. 2019; PRIMM). Explaining code in plain English
   tracks the ability to write it (Lister et al.).
5. **Give beginners a picture of the machine.** Notional machines (du Boulay; Sorva 2013) and
   Python Tutor's step-through view. For recursion, the "copies" model is the one successful
   students hold (Götschi, Sanders & Galpin 2003).
6. **Bridge reading and writing with Parsons problems.** Same learning gains as writing the code,
   in less time (Ericson et al. 2017). Faded Parsons (reorder lines and fill blanks) beat code
   writing and tracing for learning patterns in a 237-student study (Weinman et al. 2021).
7. **Space practice out; don't over-practise in one sitting.** Self-testing and spaced practice
   are the two "high utility" techniques (Dunlosky et al. 2013). Six extra same-session problems
   added nothing, while spacing had a large effect four weeks later (Rohrer & Taylor 2006).
   Duolingo's trainable spacing model lifted practice retention in A/B tests (Settles & Meeder 2016).
   Practising a harder skill can count as review of the easier skills inside it (Math Academy's
   implicit repetition).
8. **Mix only what has been learned.** Interleaving trains telling apart kinds of problems you
   already know: 72% vs 38% on a delayed test (Rohrer, Dedrick & Burgess 2014). Experts sort
   problems by underlying principle, novices by surface story (Chi, Feltovich & Glaser 1981).
9. **Help by stage, keep hints active, slow the click-through.**
   - Teaching an explicit problem-solving process, and prompting reflection when students ask for
     help, raised productivity, independence and self-efficacy (Loksa et al. 2016).
   - Hints plus self-explanation prompts carried over to a later task; hints alone didn't
     (Marwan, Williams & Price 2019).
   - Clicking quickly through to the answer is "gaming the system" and goes with less learning
     (Baker et al. 2004; up to 36% of actions in one tutor, per Aleven et al. 2006).
   - A bottom-out hint used thoughtfully works like a worked example (Shih, Koedinger & Scheines
     2008), and doing beats viewing (Naps et al. 2002).
   - Trying first helps understanding (Sinha & Kapur 2021), but beginners learn well from worked
     examples. So: no waiting timer, a free first step that asks for an action, and the answer at
     the end of a short ladder.
10. **After help, re-solve later.** Implement the solution yourself after reading it, and ask how
    you would have found it (USACO Guide: Benjamin Qi, Michael Cao). Exercises are practice, not
    targets (Erickson).
11. **Plain-language error messages** with context and a next step (Becker et al. 2019).

## Phase 1: Starting check and first hour

### What the learner gets

- **First visit** (no placement record, no problem results, no walkthrough progress and no drill
  runs): home redirects to `#/start`,
  "Where are you starting?", with three choices and a skip link:
  - **I'm new to programming:** the interim page until Phase 4, then Stage 0.
  - **I can write some Python:** the Python ready check (6 questions), then Stage 1–2 topic
    questions.
  - **I've done DSA before:** one question per topic across Stages 1–4, to map gaps.
  - **I can program, show me everything:** skip.
- **The check** shows one question per screen in the drill style: code when there is some, 2–5
  options, and the explanation after answering (green or red, as in drills and walkthrough checks).
  "Stop here" is always available and places you with what you've answered so far.
  - Ready check: missing 2 or more of the 6 suggests the new-to-programming path, with
    "Continue anyway".
  - "Some Python": each Stage 1–2 topic asks its first question and, if that's right, its second.
    A topic is placed out when both are right. The check stops after the second topic that isn't
    placed out. At most 28 questions.
  - "Done DSA": each Stage 1–4 topic asks its first question only, with no early stop.
    At most 25 questions.
- **The result screen** lists the placed-out topics and the start topic, with "Start here" (the
  start topic's first step). "Retake the starting check" lives on home.
- **Placed-out topics** get a "Placed out" tag on home and a note on the topic page: "You placed out
  of this. Everything stays open." `nextUp()` skips them. No problems are marked solved and no drills
  marked solid.
- **Interim page** (new to programming, before Phase 4): what Trace expects you to read and write
  (the six ready-check skills in plain words), plus three free courses that teach them: the official
  Python tutorial (docs.python.org/3/tutorial), Harvard's CS50P (cs50.harvard.edu/python) and Python
  for Everybody (py4e.com). Links open outside Trace. "Take the ready check" sits at the bottom.
- **Big-O comes first.** Topics 01 and 02 swap places (`01_big_o_in_practice`,
  `02_python_toolkit`), so a learner's first drill is *Read the loop*. The two Big-O hints that
  mention `Counter` (`count_bad_pairs`, `top_visitors`) are reworded to "a dict of counts", since
  Counter is introduced in the toolkit topic.
- **"Today" card on home.** The hero's Start/Continue button moves into a card at the top, showing
  the next step. If there is progress but no placement, the card also offers "Take the starting
  check". Phase 2 adds reviews to the same card.
- **Spot the pattern uses reached topics only.**
  - A topic counts as reached when any of these is true: it's placed out, one of its drills has
    been run, its walkthrough has been started, or one of its problems has a passing test.
  - Questions and wrong options both come from reached patterns only.
  - The drill opens once 4 patterns are reached. Until then the home row says "Opens after four
    pattern topics (k of 4)".

### Content: `course/starting_check.py`

Plain Python data, validated by the server like walkthroughs:

```python
"""Where are you starting?"""

READY = [
    {
        "skill": "names",    # one question per skill: names, loops, functions, lists, dicts, objects
        "code": "x = 3\nx = x + 2\nprint(x)",
        "options": ["3", "5", "x + 2"],
        "answer": 1,
        "explain": "The second line reads x (3), adds 2, and points x at the result, 5.",
        "output": True,      # --check runs the code and compares its output with options[answer]
    },
    # six in all, matching Stage 0's topics: names and values, choices and loops,
    # return vs print, lists, dicts, objects (e.g. what a.next.val prints)
]

TOPICS = {
    "01_big_o_in_practice": [
        {
            "question": "How many times does work() run?",
            "code": "for i in range(n):\n    for j in range(i):\n        work()",
            "options": ["n", "about n²/2", "n log n", "2n"],
            "answer": 1,
            "explain": "0 + 1 + … + (n−1) = n(n−1)/2, which grows like n².",
        },
        # exactly two per topic
    ],
    # every topic in Stages 1–4
}
```

Validation:
- Every question has 2–5 `options`, an `answer` that indexes them, and an `explain`.
- Every `TOPICS` key is a real topic id, and every Stage 1–4 topic has exactly two questions.
- `READY` has exactly six, one per skill.
- A question marked `"output": True` must print exactly `options[answer]` (checked by `--check`).

### Placement rule

`place(door, ready, answers, topic_order)` is a pure function returning
`{"start", "placed_out"}`. A topic is placed out when at least one question was asked about it
and every question asked was answered right. Topics the check never reached are not placed out.
The start is the first topic, in course order, that isn't placed out.

### Server

- `parse_starting_check(path)` loads and validates the file. `GET /api/starting-check` returns it.
- `POST /api/placement {"door", "ready": {skill: true|false}, "answers": {topic_id: [true, false]}}`
  stores `progress["placement"] = {"door", "date", "ready", "placed_out", "start"}`. Phase 4 uses
  the per-skill `ready` results to place out Stage 0 topics.
  - Door `"skip"` stores `{"door": "skip", "date"}`.
  - Door `"new"` stores `{"door": "new", "date"}` and has no start until Phase 4.
  - A retake overwrites the record.
- `load_progress()` defaults `placement` to `None`. `/api/reset-progress` clears it.
- `--check` validates the file and runs the `output` questions in the sandbox.
- The topic swap: rename the two folders, and swap `n` between the `python-costs` and `big-o` drill
  topics in `web/topics/foundations.js`. Problem names don't change, so saved code, progress and
  study plans are unaffected.

### Frontend

- New `web/start.js`: `T.mountStart(container, check, {onPlaced})` runs the screens, the stop rules
  and the result screen. It's a separate file so `app.js` doesn't grow, as with `walkthrough.js`.
- `app.js`:
  - the `#/start` route and the first-visit redirect;
  - `nextUp()` skips placed-out topics;
  - the Today card, the "Placed out" tags and the topic-page note;
  - `T.reachedTopics()` for the Spot-the-pattern filter.
- `web/topics/review.js` gains a pattern-to-topic map and filters by reached topics.

| Pattern keys | Topic |
|---|---|
| hash | 04 |
| two | 06 |
| window | 07 |
| prefix | 08 |
| bs, bsAns | 09 |
| sort | 10 |
| greedy | 11 |
| stack, stackPlain | 12 |
| deque | 13 |
| fastslow | 14 |
| heap | 17 |
| trie | 18 |
| bfs, dfs | 19 |
| topo, uf | 20 |
| dijkstra | 21 |
| back | 22 |
| dp | 23 |
| bits | 25 |

### Tests

- `tests/test_starting_check.py`:
  - validation errors: bad answer index, unknown topic, wrong question count;
  - `place()` for each door: all right, a miss on the first topic, stopping after the second miss,
    and skip.
- `python server.py --check` passes, including the output questions.
- Manual:
  - fresh progress through each door, the result screen and "Start here";
  - retake, skip, the placed-out tags and the topic-page note;
  - Spot the pattern before and after four reached topics;
  - light and dark mode, and phone width.

## Phase 2: Review queue

### What the learner gets

- The Today card shows "**3 reviews for today**" with a Start button. At most 5 show per day. When
  more are waiting, finishing today's set offers "Do 5 more".
- **Reviewing a problem** opens the workspace in review mode (`#/p/<name>/review`):
  - a blank starter, with a banner: "Solve it again from scratch. Your earlier solution is kept.";
  - passing every test records a pass: "Remembered. Next review in 21 days.";
  - "Not today" moves the review to tomorrow without changing its schedule;
  - using a hint (beyond Phase 3's free first step) or the solution makes it a miss. The banner says
    this up front.
- **Reviewing a drill** is one run. A clean run is a pass; any slip is a miss.
- **A drill becomes solid** after clean runs on three different days. The pips stay as they are.
  After a clean run on a day that already has one, the drill says "Come back tomorrow for the next
  clean run."

### Scheduling

- Items sit in boxes. The interval for each box, in days: `[1, 3, 7, 21, 60, 120]`.
- **Entering the queue:**
  - a first unaided solve enters at box 2 (7 days);
  - a solve after help (Phase 3) enters at box 1 (3 days);
  - a drill that turns solid enters at box 2;
  - builds and Parsons exercises never enter.
- **Pass** moves an item up one box (max 5). **Miss** moves it down two (min 0). **Not today** sets
  it due tomorrow.
- **Implicit credit:** passing a problem (a first solve or a review) also passes every *due* review
  of a lower-ranked problem in the same topic (snippet < guided < easy < medium < hard).
- **Today's list:** due items, most overdue first, with drills before problems on ties. Capped at
  5, plus 5 per "Do 5 more".
- Each item keeps its last 20 outcomes. A smarter scheduler (FSRS) can replace the interval rule
  later without changing the data.

### Data (`progress.json`)

```json
"drills": {"big-o/loops": {"runs": 4, "clean_days": ["2026-10-14", "2026-10-16"]}},
"reviews": {
  "p:two_sum":     {"box": 2, "due": "2026-10-23", "log": [["2026-10-16", "solve"]]},
  "d:big-o/loops": {"box": 2, "due": "2026-10-24", "log": [["2026-10-17", "solid"]]}
}
```

Drill keys stay `<drill topic id>/<drill id>`, as in localStorage today. Dates are the learner's
local date, sent by the browser as `today` (`YYYY-MM-DD`). The server falls back to its own date if
none is sent.

### Server

- New `review_queue.py`, pure functions with no I/O:
  - `enter`;
  - `record` (pass, miss or later);
  - `credit` (implicit credit);
  - `today_list(reviews, today, limit)`;
  - `drill_solid(record)`.

  `server.py` calls them inside `update_progress`.
- Drill progress moves to the server:
  - `POST /api/drill-result {"drill", "clean", "today", "review"}`;
  - `POST /api/drills-import {"drills"}` does a one-time import of the localStorage store.
    Records with 3 or more clean runs are stored with `"solid": true`, since they have no dates;
    the rest keep their counts.
- `/api/course?today=` adds `"reviews_today": {"items": [...], "waiting": n}`.
- `/api/test` gains `"mode": "review"`:
  - code saves to `workspace/code/review/<name>.py`, and the normal saved file is untouched;
  - the problem's own progress doesn't change;
  - a full pass records a review pass and deletes the review file.
- `POST /api/review-result {"item", "outcome", "today"}` handles "Not today" and misses.
- `record_result()` enters a problem into the queue on its first full solve.
- `/api/reset-progress` also clears `drills` and `reviews`.

### Frontend

- `web/drill.js`: `T.DrillProgress` keeps its API (`rec`, `solid`, `topicSolid`, `record`, `reset`)
  but reads `S.progress.drills` and posts results. The first boot after the update imports the
  localStorage store once, and leaves the old key in place.
- New `web/queue.js`: the review part of the Today card, the `#/review` list, and moving from one
  review to the next.
- `app.js`:
  - routes `#/review`, `#/p/<name>/review` and `#/d/<topic>/<drill>/review`;
  - the review banner in the workspace.

### Tests

- `tests/test_review_queue.py`:
  - entering the queue; pass, miss and later; box bounds;
  - implicit credit applies only to due, lower-ranked items in the same topic;
  - today's ordering and cap;
  - a drill turning solid only across three days;
  - the import rule.
- Manual:
  - a solve makes a review appear 7 days later (send a later `today`);
  - review pass, miss and "Not today";
  - a drill turning solid across days;
  - importing an old localStorage store;
  - reset.

## Phase 3: Help that teaches

### What the learner gets

- **"I'm stuck"** replaces "Show hint" on problems and guided steps. It first asks *where* you're
  stuck:

  | Choice | What it shows |
  |---|---|
  | I don't get the problem | "Work the first example by hand, one step at a time. Then make up a smaller input and solve it too." |
  | I don't know how to start | "Say the brute force first: what would you try if speed didn't matter? Then look for the work it repeats." Also the topic's *Reach for it when* and *True at every step* from its drill topic. DP topics (23, 24, 28, 34) add the SRTBOT checklist: subproblems, relation, order, base cases, original problem, time. |
  | I know the idea but can't write it | "Write the slow version and get one test passing, then change one thing at a time." Also a link to the topic's *Read the code* walkthrough, if it has one. |
  | A test fails | "Open the first failing test. Call your function on that input with Try a call and print what should change. Find the first line where it differs from your plan." Also the test's note, if it has one. |

  This first step is free: nothing gates it and it doesn't count as help.
- **Then a short ladder.** Steps 2 and 3 each open only after a Run since the previous step was
  shown:
  2. **Key idea:** the problem's (or step's) existing hint.
  3. **Rebuild it:** the reference solution as a Parsons puzzle. Its lines are shuffled, and lines
     marked as skeleton stay pinned in place. Check runs it as a dry run. Counts as help.
  4. **Solution:** a link to the Solution tab. The tab keeps its current gate and can still be
     opened at any time. Opening it before solving counts as help.

  A problem without a hint skips step 2, and one without a reference solution has no steps 3
  and 4. On guided problems, step 2 uses the current step's hint; steps 3 and 4 cover the whole
  problem.
- After steps 2 and 3, an optional one-line box asks "In your own words: what will you do next?"
  Answers are kept in localStorage per problem.
- **Solved with help:**
  - a problem solved after step 3 or 4 shows a half-filled state;
  - it enters the review queue at box 1 (3 days);
  - a review pass clears the state.
- **Plain-language errors:** a short note above the traceback for the commonest beginner errors.
  - Each note says what happened and what to check, in a neutral tone and at most two sentences.
  - The table is abridged; final wording is part of the plan.

| Error | Note (abridged) |
|---|---|
| `NameError` | Python doesn't know this name here. Check the spelling and that it's assigned before this line. |
| `UnboundLocalError` | It's assigned later in this function, so it's local everywhere in it. Give it a value first. |
| `IndentationError`, `TabError` | This line's indentation doesn't match its block. Use 4 spaces, and don't mix in tabs. |
| `SyntaxError` | Python couldn't read this line: a missing `:`, bracket or quote, or `=` where `==` was meant. Often the cause is on the line above. |
| `IndexError` | That position doesn't exist; valid indexes run from 0 to len − 1. Check loop bounds, `i + 1`, and empty input. |
| `KeyError` | The dict has no such key. Check with `in`, use `.get(key, default)`, or use a `defaultdict`. |
| `TypeError` involving `None` | A value is `None`. That comes from a function without `return`, or from `sort()`, `append()` or `reverse()`, which return nothing. |
| `AttributeError` on `None` | You went past the end of a list or tree. Check the node isn't `None` before using it. |
| `TypeError` mixing `str` and `int` | Convert first: `str(n)` to join text, `int(s)` to do arithmetic. |
| `TypeError: unhashable type` | A list can't be a dict key or set item. Use a tuple instead. |
| `RecursionError` | The function never stopped calling itself. Check the base case, and that each call works on a smaller input. |
| `ValueError` from `max()` or `min()` | The sequence was empty. Handle that case first, or pass `default=`. |

### Server and runner

- `runner/judge.py`: `explain_error(exc)` matches the exception type plus a message pattern and
  returns a note or `None`. The note is attached wherever a user exception becomes an error:
  `error_note` next to `error` (tests and custom calls), and `load_note` next to `load_error`.
  Same idea as the existing `explain_mismatch`.
- `POST /api/help {"name", "rung"}` records the highest step used in
  `progress["problems"][name]["help"]`. Step 3 or above before the first solve sets
  `"helped": true`.
- `record_result()` uses `helped` to pick the entry box (1 vs 2). A review pass clears `helped`.

### Frontend

- New `web/hints.js`: `T.mountHelp(container, problem, ctx)` holds the stage chooser, the ladder,
  the run gating (it listens for the workspace's run event) and the explanation boxes.
- New `web/parsons.js`: `T.mountParsons(container, {lines, pinned, blanks}, {onCheck})`.
  - Lines keep their indentation: learners order lines, they don't indent them.
  - Blanks (`___`) become small inputs.
  - Reorder by dragging, or with Alt+↑/↓ on a focused line.
  - Phase 4's exercises reuse it.
- `app.js`:
  - swaps the hint buttons for the help panel;
  - renders `error_note` and `load_note` above tracebacks;
  - shows the solved-with-help state in item rows and stepper pills.

### Tests

- `tests/test_errors.py`: each table row maps to its note, and unrelated errors get none.
- Help recording:
  - the highest step is kept;
  - `helped` is set only before the first solve;
  - the entry box is 1 vs 2 accordingly, and a review pass clears it.
- Manual:
  - each stuck choice;
  - gating: step 3 stays closed until a Run;
  - Rebuild with and without skeleton marks;
  - solution, then solved with help, then a review 3 days later;
  - the error notes, on code written to fail.

## Phase 4: Beginner content

### Stage 1 walkthroughs

*Read the code* for all five Stage 1 topics, in the existing walkthrough format:

| Topic | Layers |
|---|---|
| 01 Big-O | count a loop's steps; nested loops; a halving loop; reading the input limit |
| 02 Python toolkit | list costs; dict and set; Counter and defaultdict; deque; sorting with a key |
| 03 Arrays and strings | index arithmetic (where does index i land after rotating by k?); a write index that keeps what you want in one pass (move zeroes); a left pass and a right pass (product except self, as the reuse screen) |
| 04 Hashing | a seen set (first repeat); counting with a dict; remembering what you've seen to look up the complement (two sum); choosing the key (group anagrams, as the reuse screen) |
| 05 Recursion | each call printed as its own indented copy, with its arguments and return value (the "copies" model) |

Each walkthrough ends with one **in plain English** check: "Which sentence says what this code
does?" The right option describes its purpose; the wrong ones restate it line by line or describe
a near miss.

### Stage 0: Python from zero

`course/0_python_from_zero/` holds six topics on the usual ladder: drills, Read the code, Put it
together, Snippet, Guided, and 3–5 easy problems. No hard problems and no build.

| Topic | Covers |
|---|---|
| P1 Names and values | names pointing at values, reassignment, int/float/str/bool, f-strings |
| P2 Choices and loops | if/elif/else, `and`/`or`/`not`, while, for with range, keeping a running total |
| P3 Functions | def, parameters, return vs print, `None`, local names |
| P4 Lists | 0-based and negative indexes, slices, append and pop, looping, 2D lists, two names for one list |
| P5 Dicts and sets | key to value, `in`, `.get`, counting, iterating, removing duplicates |
| P6 Objects and references | a class with `__init__`, attributes, `None`, a chain of `Node`s, `while node:` |

- **Notional-machine drills** (`web/topics/python_zero.js`): names drawn as labels with arrows to
  value boxes. The learner:
  - P1: steps through code and picks a name's value after each line;
  - P2: counts loop turns and final totals;
  - P3: says what a call returns versus what it prints;
  - P4: decides "same list or a copy?";
  - P5: counts into a dict;
  - P6: follows `next` arrows.
- **A new exercise kind, `[parsons]`** ("Put it together"), using the Phase 3 widget:

```python
"""
Count the vowels                                                        [parsons]

Put the lines in order and fill the blanks so `count_vowels(s)` returns how many vowels `s` has.
"""

PARSONS = '''
def count_vowels(s):
    count = 0
    for ch in s:
        if ch in ___:
            count += ___
    return count
'''
BLANKS = ['"aeiou"', "1"]      # the reference fill: --check assembles PARSONS with it and runs TESTS

TESTS = [(("banana",), 3), (("",), 0)]
```

  - `KINDS` gains `"parsons"` before `"snippet"`, and the header tag pattern accepts it.
  - It doesn't lock anything and isn't locked. On the topic page it's its own rung, "Put it
    together", between Read the code and Snippet.
  - The workspace shows the widget in place of the editor. `/api/solution` returns the assembled
    reference.
  - `--check` assembles `PARSONS` with `BLANKS` and requires every test to pass. The
    "starter reports todo" check is skipped for this kind.
- **Numbering:** Stage 0 folders use a `P<k>_` prefix (`P1_names_and_values`).
  - When a folder's prefix isn't a number, the server reads `n` as text (`"P1"`).
  - `check()`'s label formatting accepts text.
  - Drill topics use `n: "P1"` and so on.
- **Placement:**
  - "New to programming" now starts at P1 instead of showing the interim page.
  - "Some Python": each ready-check skill maps to its Stage 0 topic (names → P1, loops → P2,
    functions → P3, lists → P4, dicts → P5, objects → P6). The usual rule applies: a right answer
    places that topic out. Someone who misses a skill and chooses "Continue anyway" starts at the
    first Stage 0 topic they missed. "Open anyway" and the topic list still let them go anywhere.
  - "Done DSA" and skip mark every Stage 0 topic as placed out.
- Problem names stay unique across the course, because the server keys problems by file name.

### Tests

- `--check` passes for every new walkthrough and every Parsons exercise. Stage 0 problems pass like
  any others.
- New `tests/test_parsons.py`: the parsons parser (blank count must match `BLANKS`) and the `P1`
  folder numbering.
- Manual:
  - the full Stage 0 ladder for P1;
  - "New to programming" starts at P1;
  - the other choices show Stage 0 as placed out;
  - each walkthrough's plain-English check.

## Success criteria

- A first-time user lands on "Where are you starting?" and, by any route, ends on a named next
  step in 28 questions or fewer.
- A "some Python" learner's first drill is *Read the loop*.
- No drill becomes solid in a single day.
- Every solved snippet, guided or solo problem has a scheduled review, and no more than 5 reviews
  show per day unless the learner asks for more.
- Ladder steps 2 and 3 never open without a Run since the previous step. Using Rebuild or the
  solution before solving schedules a re-solve 3 days later.
- Every error in the table shows its note.
- `python server.py --check` covers the starting check, walkthroughs and Parsons exercises. Unit
  tests cover placement, the review queue and the error notes.

## Considered and left out

- **Timing feedback from doubling the input size** (Sedgewick & Wayne's doubling test): it needs
  an input generator for every guided problem. Revisit after Phase 3.
- **A line-by-line stepper** (Python Tutor style): a separate project. The Stage 0 drills cover the
  machine picture for chosen code. It was also out of scope in the Read-the-code spec.
- **Streaks, badges and reminders:** they cut against the calm design. Gamification's effects on
  motivation and behaviour are small and unstable in the more careful studies (Sailer & Homner
  2020). Behavioural nudges in MOOCs lost most of their effect at scale (Kizilcec et al. 2020).
- **FSRS scheduling:** fixed intervals first. The outcome log keeps the option open.
- **Free-text "explain in plain English" with automatic grading** (Fowler et al. 2021): multiple
  choice instead.
- **Problem-count targets** (interviewing.io's data on practice volume): they're about interview
  preparation, not getting started.

## References

- Aleven et al. 2006, help abuse: [LearnLab summary](https://learnlab.org/research/wiki/index.php/Help_abuse)
- Baker, Corbett, Koedinger & Wagner 2004, gaming the system: [CHI paper](https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p383.pdf)
- Bandura 1977, sources of self-efficacy: [summary](https://www.simplypsychology.org/self-efficacy.html)
- Becker et al. 2019, programming error messages: [review](https://neverworkintheory.org/2021/09/02/compiler-error-messages-considered-unhelpful.html)
- Chi, Feltovich & Glaser 1981: [abstract](https://education.asu.edu/lcl/publications/chi-m-t-h-feltovich-p-glaser-r-1981-categorization-and-representation-physics)
- Dunlosky et al. 2013: [APS summary](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)
- Ericson, Margulieux & Rick 2017, Parsons problems: [summary](https://hg.gatech.edu/node/603172)
- Erickson, *Algorithms*, "About the Exercises": [front matter](https://jeffe.web.engr.illinois.edu/teaching/algorithms/book/!!-frontmatter.pdf)
- Expertise reversal effect: [overview](https://en.wikipedia.org/wiki/Expertise_reversal_effect)
- Fowler et al. 2021, automatic grading of plain-English explanations: [paper](https://zilles.web.engr.illinois.edu/papers/fowler_EiPE_NLP_SIGCSE_2021.pdf)
- FSRS: [project](https://github.com/open-spaced-repetition/fsrs4anki)
- Götschi, Sanders & Galpin 2003, mental models of recursion: [abstract](https://homepages.inf.ed.ac.uk/vgalpin1/pubs/GSG03.html)
- Guo 2013, Online Python Tutor: [paper](https://research.google/pubs/online-python-tutor-embeddable-web-based-program-visualization-for-cs-education/)
- Khan Academy mastery and course challenges: [help page](https://support.khanacademy.org/hc/en-us/articles/115002552631)
- Kizilcec et al. 2020, behavioural interventions in online education: [PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC7334459)
- Kulik, Kulik & Bangert-Drowns 1990, mastery learning: [paper](https://www.academia.edu/81783373/Effectiveness_of_Mastery_Learning_Programs_A_Meta_Analysis)
- Lister et al., explaining code vs writing it: [paper](https://opus.lib.uts.edu.au/handle/10453/22969)
- Loksa et al. 2016, explicit problem-solving instruction: [paper](https://faculty.washington.edu/ajko/papers/Loksa2016ProgrammingProblemSolving.pdf)
- Lopez et al. 2008, reading, tracing and writing: [paper](https://opus.lib.uts.edu.au/bitstream/10453/10806/1/2008001530.pdf)
- Marwan, Williams & Price 2019, programming hints: [paper](https://isnap.csc.ncsu.edu/home/public/publication/marwan-2019-icer)
- Math Academy (Skycak), spaced repetition over a knowledge graph: [article](https://gwern.net/doc/www/www.justinmath.com/9af2ce40376e836660c237a0e971d1896a163eee.html)
- MIT 6.006, SRTBOT: [lecture notes](https://live.ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/665523227a175e9e9ce26ea8d3e5b51c_MIT6_006S20_lec17.pdf)
- Naps et al. 2002, visualization and engagement: [DOI](https://doi.org/10.1145/960568.782998)
- PRIMM: [summary](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)
- Rohrer, Dedrick & Burgess 2014, interleaved practice: [paper](https://link.springer.com/article/10.3758/s13423-014-0588-3)
- Rohrer & Taylor 2006, overlearning and spacing: [paper](https://digitalcommons.usf.edu/psy_facpub/1770/)
- Sailer & Homner 2020, gamification meta-analysis: [paper](https://link.springer.com/article/10.1007/s10648-019-09498-w)
- Sedgewick & Wayne, doubling test: [DoublingRatio](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/DoublingRatio.html)
- Settles & Meeder 2016, Duolingo spacing model: [paper](https://preview.aclanthology.org/landing_page/P16-1174), [Duolingo blog](https://blog.duolingo.com/how-we-learn-how-you-learn)
- Shih, Koedinger & Scheines 2008, bottom-out hints: [paper](https://www.cmu.edu/dietrich/philosophy/docs/scheines/Shih_Koedinger_Scheines_2008_EDM.pdf)
- Sinha & Kapur 2021, problem solving before instruction: [summary](https://education.utexas.edu/about/deans-office-units/office-instructional-innovation/instruction-then-problem-solving-or-vice-versa)
- Sorva 2013, "Notional Machines and Introductory Programming Education", *ACM Transactions on
  Computing Education* 13(2)
- UBC CPSC 320, "How to Solve a 320 Problem": [handout](https://blogs.ubc.ca/cpsc320/files/2016/09/how-to-solve-320-problems.pdf)
- USACO Guide: [Expected Knowledge](https://usaco.guide/general/expected-knowledge), [Practicing](https://usaco.guide/general/practicing)
- Weinman, Fox & Hearst 2021, faded Parsons problems: [paper](https://acelab.berkeley.edu/wp-content/papercite-data/pdf/parsons-chi2021.pdf)
- Wiedenbeck et al. 2004, self-efficacy and mental models: [paper](https://ppig.org/papers/2004-ppig-16th-wiedenbeck/)
- Xie et al. 2019, a theory of instruction for programming: [paper](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)
