# Beginner path: start anywhere, keep what you learn

**Status:** draft for review. Rewritten 2026-10-16 after checking every cited claim against its
source; the "Evidence check" section lists what changed.
**Scope:** four phases. Each ships on its own and gets its own implementation plan:

1. Starting check and first hour
2. Reviews and mixed practice
3. Help that teaches
4. Beginner content

## Goal

Anyone who opens Trace, from someone who has never programmed to someone who has done DSA before,
should:
- know where to start within a few minutes;
- get a real win in the first session;
- learn more per hour, by spending time on the practice research shows works best;
- still remember week-one material a month later.

The 34-topic ladder stays the core. This work adds a way in (placement and a floor), a way back
(reviews and mixed practice), and help that teaches instead of only revealing.

## Assumptions

- **Both kinds of beginner, in stages.** Phases 1–3 serve learners who can already write some
  Python. Phase 4 adds Stage 0 for people who can't. Until Phase 4 ships, the "new to programming"
  choice shows an interim page.
- Trace stays offline, single-user and Python-only.
- **Calm**, per the restyle spec: no streaks, badges or reminders. Progress is shown, not pushed.
- Content (check questions, walkthroughs, Stage 0 exercises) is written during each phase's plan,
  in the formats defined here.
- **Numbers are starting values.** Review intervals, the daily cap and question counts are design
  choices, not research results. They're tuned with use (see "How we'll know it's working").

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
- Practice is always grouped by topic, and the topic is always on screen. *Spot the pattern* is the
  only mixed practice, and it samples all 36 of its questions, so a learner three topics in mostly
  meets techniques they haven't learned.

## What helps learning most, and how sure we are

Ordered by expected effect on learning. Strength labels:
- **Strong:** meta-analyses or repeated experiments.
- **Moderate:** one or two solid studies, or a strong correlation.
- **Mixed:** studies disagree.
- **Untested:** a design idea with no published evaluation.

1. **Space practice out, and practise by recalling.** Strong.
   - Self-testing and spaced practice are the only two of ten study techniques rated "high utility"
     (Dunlosky et al. 2013).
   - Spacing maths practice over two sessions made no difference at one week but a very large one
     at four weeks. Six extra problems in the same sitting had no effect at one or four weeks
     (Rohrer & Taylor 2006).
   - *Used in:* Phase 2. Reviews are re-solves from a blank editor, spread out in time.
2. **Worked examples first, then fade the support.** Strong.
   - Beginners learn more from studying worked solutions. The advantage shrinks and then reverses
     as they gain expertise (worked-example and expertise-reversal effects).
   - Trace's ladder already fades support: Read the code, Snippet, Guided, Problems. Phase 4 adds
     Put it together between reading and writing.
   - *Used in:* Phase 1 (placement skips support you no longer need) and Phase 4 (walkthroughs and
     Parsons exercises where beginners start).
3. **Mix problem types once each is learned.** Strong in maths; untested for programming.
   - Grade 7 students practised for nine weeks. On an unannounced test two weeks later they scored
     72% on material practised mixed and 38% on material practised in blocks (d = 1.05). Mixing
     forces you to choose the strategy, and the effect held even when the problem types looked
     different from each other (Rohrer, Dedrick & Burgess 2014).
   - *Used in:* Phase 2 (mixed sets with topics hidden; reviews mix topics) and Phase 1 (Spot the
     pattern only uses topics you've reached).
4. **Move on after mastery, but keep the locks soft.** Strong.
   - Mastery programmes raised exam scores across 108 controlled studies, more for weaker students.
     Self-paced versions often lowered completion in college courses (Kulik, Kulik &
     Bangert-Drowns 1990).
   - *Used in:* placement, the ladder, and keeping "Open anyway".
5. **Try first, but don't stay stuck.** Strong.
   - Problem solving before instruction beat instruction first, g = 0.36 across 53 studies, and more
     when designed carefully. Young children and domain-general skills did better with instruction
     first (Sinha & Kapur 2021).
   - Together with point 2: no waiting timer, a free first help step that asks for an action, and
     the answer at the end of a short ladder.
   - *Used in:* Phase 3.
6. **Read and trace code before writing it.** Moderate.
   - Scores on tracing and explaining together accounted for 46% of the variation in code-writing
     scores (Lopez et al. 2008). The same pattern held in data-structures exams (Pelchen, Mathieson
     & Lister). The exact ordering of these skills did not replicate everywhere (Hassan et al.).
   - Teaching tracing, syntax, reading patterns and writing as separate steps, in that order,
     improved completion, cut errors, and improved post-test understanding (Xie et al. 2019).
   - Explaining code in plain English correlates strongly with writing it (Murphy, Fitzgerald,
     Lister & McCauley 2012). That's a correlation, not proof that practising one improves the other.
   - *Used in:* Phase 4 (walkthroughs, predict-then-run, plain-English checks, Stage 0 drills).
7. **Bridge reading and writing with Parsons problems.** Moderate.
   - Putting given lines in order took less time than writing or fixing the code, with the same
     learning gains (Ericson, Margulieux & Rick 2017).
   - Faded Parsons (reorder lines and fill blanks) beat code writing and code tracing for learning
     patterns, and matched code writing for general writing skill, in a 237-student study (Weinman,
     Fox & Hearst 2021).
   - *Used in:* Phase 3 (Rebuild step) and Phase 4 (Put it together).
8. **Teach an explicit problem-solving process.** Moderate (small study, different setting).
   - Explicit instruction in problem-solving stages, a view of progress through them, and reflection
     prompts when asking for help raised productivity, independence and self-efficacy. The study ran
     with 48 high-schoolers in web-development camps (Loksa et al. 2016).
   - Expert courses teach similar steps (UBC CPSC 320's handout).
   - *Used in:* Phase 1 ("How to work a problem") and Phase 3 ("I'm stuck").
9. **Make hints active, and slow the click-through.** Mixed.
   - Hints with explanations helped on the spot, but carried over to a later task only when combined
     with self-explanation prompts. That study used block-based programming with online participants
     (Marwan, Williams & Price 2019). A classroom follow-up found the improved hints raised
     assignment scores but didn't significantly improve learning (Marwan et al. 2023).
   - "Gaming the system", such as clicking through hints to the answer, went with substantially
     less learning (Baker et al. 2004).
   - Shih, Koedinger & Scheines (2008) argue that a final hint used thoughtfully works like a worked
     example.
   - *Used in:* Phase 3.
10. **Give beginners a picture of the machine.** Moderate (conceptual).
    - Beginners need an explicit model of what the computer does when code runs: a "notional
      machine" (du Boulay; Sorva 2013).
    - For recursion, the "copies" model is the viable one, meaning it represents recursion
      accurately and consistently, and most students in the study built it (Götschi, Sanders &
      Galpin 2003).
    - *Used in:* Phase 4 (Stage 0 drills, the recursion walkthrough).
11. **An early, real success.** Moderate.
    - Bandura's theory names mastery experiences as a source of self-efficacy, and reviews of school
      research usually find it the strongest.
    - Self-efficacy and a working mental model both had direct effects on success in an intro
      programming course (Wiedenbeck et al. 2004).
    - *Used in:* Phase 1 (Big-O first, start at your first gap).
12. **Plain-language error messages.** Mixed.
    - There are design guidelines (Becker et al. 2019). One controlled study found enhanced messages
      had no significant effect (Denny, Luxton-Reilly & Carpenter 2014). A later Java study found
      fewer repeated errors for some messages (Becker et al. 2016).
    - Cheap to add, so worth doing, but don't expect much.
    - *Used in:* Phase 3.

**Not adopted:**
- Streaks and gamification: small effects, and the motivational and behavioural effects were
  unstable in the more careful studies (Sailer & Homner 2020).
- Plan-making nudges and reminders: they raised engagement for a few weeks but not completion, and
  effects shrank roughly tenfold at scale (Kizilcec et al. 2020).
- A model-based scheduler as a first step: Duolingo's model predicted recall better than the
  Leitner boxes it replaced, but its A/B tests measured next-day return, not learning, with mixed
  results (Settles & Meeder 2016). Simple boxes come first.

## Phase 1: Starting check and first hour

### What the learner gets

- **First visit** (no placement record, no problem results, no walkthrough progress and no drill
  runs): home redirects to `#/start`, "Where are you starting?", with three choices and a skip link:
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
- **"How to work a problem."** The first time a learner opens a problem, a short card explains the
  four stages used everywhere in Trace. It can be dismissed, and reopened from a workspace link and
  (Phase 3) from "I'm stuck".
  1. **Understand:** work the example by hand, then make up a smaller input and solve that too.
  2. **Plan:** say the brute force first, then look for the work it repeats.
  3. **Code:** write the slow version and get one test passing, then change one thing at a time.
  4. **Check:** open the first failing test, run your function on it with Try a call, and find
     where it differs from your plan.
- **"Today" card on home.** The hero's Start/Continue button moves into a card at the top, showing
  the next step. If there is progress but no placement, the card also offers "Take the starting
  check". Phase 2 adds reviews and mixed practice to the same card.
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

`place(door, ready, answers, topic_order)` is a pure function returning `{"start", "placed_out"}`.
A topic is placed out when at least one question was asked about it and every question asked was
answered right. Topics the check never reached are not placed out. The start is the first topic, in
course order, that isn't placed out.

### Server

- `parse_starting_check(path)` loads and validates the file. `GET /api/starting-check` returns it.
- `POST /api/placement {"door", "ready": {skill: true|false}, "answers": {topic_id: [true, false]}}`
  stores `progress["placement"] = {"door", "date", "ready", "placed_out", "start"}`.
  - Door `"skip"` stores `{"door": "skip", "date"}`.
  - Door `"new"` stores `{"door": "new", "date"}` and has no start until Phase 4.
  - A retake overwrites the record. Phase 4 uses the per-skill `ready` results.
- `load_progress()` defaults `placement` to `None`. `/api/reset-progress` clears it.
- `--check` validates the file and runs the `output` questions in the sandbox.
- The topic swap: rename the two folders, and swap `n` between the `python-costs` and `big-o` drill
  topics in `web/topics/foundations.js`. Problem names don't change, so saved code, progress and
  study plans are unaffected.

### Frontend

- New `web/start.js`: `T.mountStart(container, check, {onPlaced})` runs the screens, the stop rules
  and the result screen. It also exports `T.howToCard()`. It's a separate file so `app.js` doesn't
  grow, as with `walkthrough.js`.
- `app.js`:
  - the `#/start` route and the first-visit redirect;
  - `nextUp()` skips placed-out topics;
  - the Today card, the "Placed out" tags and the topic-page note;
  - showing the how-to card on the first problem opened (a localStorage flag), plus its workspace
    link;
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
    unreached topics not placed out, and skip.
- `python server.py --check` passes, including the output questions.
- Manual:
  - fresh progress through each door, the result screen and "Start here";
  - retake, skip, the placed-out tags and the topic-page note;
  - the how-to card on the first problem, and only then;
  - Spot the pattern before and after four reached topics;
  - light and dark mode, and phone width.

## Phase 2: Reviews and mixed practice

### What the learner gets

- **Reviews.** The Today card shows "**3 reviews for today**" with a Start button. At most 5 show
  per day. When more are waiting, finishing today's set offers "Do 5 more".
  - **Reviewing a problem** opens the workspace in review mode (`#/p/<name>/review`):
    - a blank starter, with a banner: "Solve it again from scratch. Your earlier solution is kept.";
    - passing every test records a pass: "Remembered. Next review in 21 days.";
    - "Not today" moves the review to tomorrow without changing its schedule;
    - using a hint (beyond Phase 3's free first step) or the solution makes it a miss. The banner
      says this up front.
  - **Reviewing a drill** is one run. A clean run is a pass; any slip is a miss.
  - Today's reviews come from different topics in one list, so reviewing is itself mixed practice.
- **A drill becomes solid** after clean runs on three different days. The pips stay as they are.
  After a clean run on a day that already has one, the drill says "Come back tomorrow for the next
  clean run."
- **Mixed practice.** Once a learner has learned at least three topics in a stage (Stages 1–4), the
  Today card offers "**Mixed practice: Stage 2, topics hidden**".
  - A topic counts as learned when it's placed out or one of its guided or solo problems is solved.
  - A set holds up to 5 problems: one per learned topic in turn, at most 2 per topic, in random
    order. The set stays the same all day.
  - Mixed mode (`#/mix/<stage>` lists the set; `#/p/<name>/mix/<stage>` opens one) hides everything
    that names the technique: the title (shown as "Problem 2 of 5"), the topic, the stepper, plan
    and "often reported" badges, and the "Aim for" callout. Tests, Try a call and help stay.
  - Every problem starts from a blank editor, as in review mode. A pass on an unsolved problem
    counts as its first solve; on a solved one it counts as a review pass.
  - After each pass, the screen shows what it was ("This was Sliding window: Longest substring…")
    with a link to the topic.

### Scheduling

- Items sit in boxes. The interval for each box, in days: `[1, 3, 7, 21, 60, 120]`.
- **Entering the queue:**
  - a first unaided solve enters at box 2 (7 days);
  - a solve after help (Phase 3) enters at box 1 (3 days);
  - a drill that turns solid enters at box 2;
  - builds and Parsons exercises never enter.
- **Pass** moves an item up one box (max 5). **Miss** moves it down two (min 0). **Not today** sets
  it due tomorrow.
- **Implicit credit** (an idea from Math Academy, not yet evaluated): passing a problem also passes
  every *due* review of a lower-ranked problem in the same topic (snippet < guided < easy < medium
  < hard). This applies to first solves, reviews and mixed practice.
- **Today's list:** due items, most overdue first, with drills before problems on ties. Capped at
  5, plus 5 per "Do 5 more".
- Each item keeps its last 20 outcomes. That lets a smarter scheduler (FSRS) replace the interval
  rule later without changing the data.

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
- New `mixed_sets.py`, also pure: `mixed_set(stage, today, topics, problems, progress, size=5)`
  returns problem names. It uses a shuffle seeded by stage and date, so the set is stable for the
  day.
- `server.py` calls both inside `update_progress` and the request handlers.
- Drill progress moves to the server:
  - `POST /api/drill-result {"drill", "clean", "today", "review"}`;
  - `POST /api/drills-import {"drills"}` does a one-time import of the localStorage store.
    Records with 3 or more clean runs are stored with `"solid": true`, since they have no dates;
    the rest keep their counts.
- `/api/course?today=` adds `"reviews_today": {"items": [...], "waiting": n}` and
  `"mixed_offers": [stage, ...]`.
- `GET /api/mix?stage=&today=` returns the day's set.
- `/api/test` gains `"mode": "review"` (also used by mixed practice):
  - code saves to `workspace/code/review/<name>.py`, and the normal saved file is untouched;
  - a full pass records a first solve (if unsolved) or a review pass;
  - the review file is deleted after a pass.
- `POST /api/review-result {"item", "outcome", "today"}` handles "Not today" and misses.
- `record_result()` enters a problem into the queue on its first full solve.
- `/api/reset-progress` also clears `drills` and `reviews`.

### Frontend

- `web/drill.js`: `T.DrillProgress` keeps its API (`rec`, `solid`, `topicSolid`, `record`, `reset`)
  but reads `S.progress.drills` and posts results. The first boot after the update imports the
  localStorage store once, and leaves the old key in place.
- New `web/queue.js`:
  - the review and mixed-practice parts of the Today card;
  - the `#/review` and `#/mix/<stage>` lists;
  - moving from one item to the next.
- `app.js`:
  - routes `#/review`, `#/p/<name>/review`, `#/d/<topic>/<drill>/review`, `#/mix/<stage>` and
    `#/p/<name>/mix/<stage>`;
  - the review banner, and the mixed-mode workspace that hides the labels listed above.

### Tests

- `tests/test_review_queue.py`:
  - entering the queue; pass, miss and later; box bounds;
  - implicit credit applies only to due, lower-ranked items in the same topic;
  - today's ordering and cap;
  - a drill turning solid only across three days;
  - the import rule.
- `tests/test_mixed_sets.py`:
  - only learned topics are used, and at most 2 problems per topic;
  - no set is offered below three learned topics;
  - the same set for the same stage and day, and a different set on another day.
- Manual:
  - a solve makes a review appear 7 days later (send a later `today`);
  - review pass, miss and "Not today";
  - a drill turning solid across days;
  - a mixed set hides every label, then reveals the topic after a pass;
  - importing an old localStorage store;
  - reset.

## Phase 3: Help that teaches

### What the learner gets

- **"I'm stuck"** replaces "Show hint" on problems and guided steps. It first asks *where* you're
  stuck, using the four stages from "How to work a problem":

  | Choice | What it shows |
  |---|---|
  | I don't get the problem (Understand) | "Work the first example by hand, one step at a time. Then make up a smaller input and solve it too." |
  | I don't know how to start (Plan) | "Say the brute force first: what would you try if speed didn't matter? Then look for the work it repeats." Also the topic's *Reach for it when* and *True at every step* from its drill topic. DP topics (23, 24, 28, 34) add MIT 6.006's SRTBOT checklist: subproblems, relation, order, base cases, original problem, time. |
  | I know the idea but can't write it (Code) | "Write the slow version and get one test passing, then change one thing at a time." Also a link to the topic's *Read the code* walkthrough, if it has one. |
  | A test fails (Check) | "Open the first failing test. Call your function on that input with Try a call and print what should change. Find the first line where it differs from your plan." Also the test's note, if it has one. |

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
- After steps 2 and 3, a one-line box asks "In your own words: what will you do next?" It's
  optional, and answers are kept in localStorage per problem. This is the self-explanation prompt
  that made hints carry over in Marwan et al.
- **Solved with help:**
  - a problem solved after step 3 or 4 shows a half-filled state;
  - it enters the review queue at box 1 (3 days);
  - a review pass clears the state.
- **Plain-language errors:** a short note above the traceback for the commonest beginner errors.
  - Each note says what happened and what to check, in a neutral tone and at most two sentences
    (Becker et al.'s guidelines).
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

### Walkthroughs where beginners start, then everywhere

*Read the code* for all five Stage 1 topics first, in the existing walkthrough format:

| Topic | Layers |
|---|---|
| 01 Big-O | count a loop's steps; nested loops; a halving loop; reading the input limit |
| 02 Python toolkit | list costs; dict and set; Counter and defaultdict; deque; sorting with a key |
| 03 Arrays and strings | index arithmetic (where does index i land after rotating by k?); a write index that keeps what you want in one pass (move zeroes); a left pass and a right pass (product except self, as the reuse screen) |
| 04 Hashing | a seen set (first repeat); counting with a dict; remembering what you've seen to look up the complement (two sum); choosing the key (group anagrams, as the reuse screen) |
| 05 Recursion | each call printed as its own indented copy, with its arguments and return value (the "copies" model) |

After Stage 0 (below), walkthroughs continue through Stages 2–4, one topic at a time, starting
with the most-used patterns: two pointers, prefix sums, binary search, stacks, trees, graph
traversal, 1D DP. Worked examples help most while a topic is new.

Two additions to the walkthrough format:

- **Predict, then run.** A layer may have a `predict` question ("What will this print?"). Run
  stays disabled until it's answered; then the real output shows next to the prediction. `--check`
  runs the layer's code and requires the output to equal `options[answer]`.

  ```python
  "predict": {
      "question": "What will this print?",
      "options": ["[1, 2]", "[2, 3]", "[1, 2, 3]"],
      "answer": 1,
      "explain": "The window drops 1 when it grows past size 2.",
  },
  ```

- **One "in plain English" check per walkthrough**, at the end: "Which sentence says what this code
  does?" The right option states the purpose. The wrong ones restate it line by line or describe a
  near miss.

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
  - Later, Stage 1–2 topics can gain a Put-it-together rung too, as faded versions of their
    snippets.
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

- `--check` passes for:
  - every new walkthrough, including its predict questions;
  - every Parsons exercise;
  - Stage 0 problems, like any others.
- New `tests/test_parsons.py`: the parsons parser (blank count must match `BLANKS`) and the `P1`
  folder numbering.
- `tests/test_walkthrough.py` gains validation cases for `predict`.
- Manual:
  - the full Stage 0 ladder for P1;
  - "New to programming" starts at P1;
  - the other choices show Stage 0 as placed out;
  - predict-then-run and the plain-English check in a Stage 1 walkthrough.

## Success criteria

- A first-time user lands on "Where are you starting?" and, by any route, ends on a named next
  step in 28 questions or fewer.
- A "some Python" learner's first drill is *Read the loop*, and their first problem shows the
  how-to card.
- No drill becomes solid in a single day.
- Every solved snippet, guided or solo problem has a scheduled review, and no more than 5 reviews
  show per day unless the learner asks for more.
- A mixed set never shows a problem's title, topic or technique before it's passed.
- Ladder steps 2 and 3 never open without a Run since the previous step. Using Rebuild or the
  solution before solving schedules a re-solve 3 days later.
- Every error in the table shows its note.
- `python server.py --check` covers the starting check, walkthroughs (with predict questions) and
  Parsons exercises. Unit tests cover placement, the review queue, mixed sets and the error notes.

## How we'll know it's working

The review log in `progress.json` already holds what's needed. Nothing leaves the machine.
- **Retention:** the share of review passes in each box. If passes at 21 days fall below about 80%,
  shorten the intervals; if they stay near 100%, lengthen them.
- **Help:** first-try review passes for problems solved with help vs without. This shows whether
  the ladder teaches or just reveals.
- **Mixed practice:** the pass rate in mixed sets vs within topics. A gap means recognition is still
  weak, so point the learner to Spot the pattern.
- **Starting:** how many questions the check took, and whether the first suggested step was passed
  on day one.

## Considered and left out

- **Timing feedback from doubling the input size** (Sedgewick & Wayne's doubling test): it needs an
  input generator for every guided problem. Revisit after Phase 3.
- **A line-by-line stepper** (Python Tutor style): a separate project. The Stage 0 drills cover the
  machine picture for chosen code. It was also out of scope in the Read-the-code spec.
- **Streaks, badges and reminders:** see "Not adopted" above.
- **A model-based scheduler (FSRS, or something like Duolingo's):** fixed boxes first. The outcome
  log keeps the option open.
- **Free-text "explain in plain English" with automatic grading** (Fowler et al. 2021): multiple
  choice instead.
- **Problem-count targets** (interviewing.io's data on practice volume): they're about interview
  preparation, not getting started.

## Evidence check (2026-10-16)

Every claim was checked against its source. Twelve papers were checked in full text; the rest
through abstracts or summaries, as marked in the references. What changed from the first draft:

- **Duolingo:** the first draft said their model "lifted practice retention". In fact, against the
  Leitner boxes it left overall daily return flat and *lowered* return to practice sessions by 7.3%.
  The +9.5% came from a later test between two versions of their own model. Both tests measured
  next-day return, not learning. It's now only a reason to start simple.
- **Recursion:** the "copies" model is the viable one and most students built it. The paper doesn't
  tie it to students who succeed.
- **Plain-English explanations:** the study is Murphy, Fitzgerald, Lister & McCauley (2012), and its
  result is a correlation.
- **Productive failure:** the split "better for understanding, equal for procedures" came from press
  coverage, not the paper. It's replaced with the abstract's findings: g = 0.36, stronger with
  careful design, and the cases that favoured instruction first.
- **Hint abuse ("36% of actions"):** I could only trace this to a secondary wiki, so it's removed.
- **Error messages:** added that the evidence is mixed (a controlled null result, Denny et al. 2014).
- **Hints:** added the study's setting (block-based, online participants) and the classroom
  follow-up with no significant learning gain (Marwan et al. 2023).
- **Explicit process:** added the sample and setting (48 high-schoolers, web-development camps).
- **Read before write:** added that the exact skill ordering didn't replicate everywhere.
- **Math Academy:** implicit repetition and placement are marked as unevaluated design.
- **Numbers:** intervals, the cap and question counts are marked as design choices.
- **Added for learning:** mixed practice with topics hidden (the strongest effect not yet in
  Trace), predict-then-run in walkthroughs, the "How to work a problem" card, and walkthroughs
  beyond Stage 1.

## References

Each entry is marked with how it was checked: full text, abstract, or summary (a secondary source).

- Baker, Corbett, Koedinger & Wagner 2004, gaming the system. Full text. [PDF](https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p383.pdf)
- Bandura 1977, sources of self-efficacy. Summary. [overview](https://www.simplypsychology.org/self-efficacy.html)
- Becker et al. 2019, programming error messages. Summary. [review](https://neverworkintheory.org/2021/09/02/compiler-error-messages-considered-unhelpful.html)
- Becker et al. 2016, "Effective compiler error message enhancement for novice programming
  students", *Computer Science Education* 26(2–3). Summary.
- Chi, Feltovich & Glaser 1981. Abstract. [record](https://education.asu.edu/lcl/publications/chi-m-t-h-feltovich-p-glaser-r-1981-categorization-and-representation-physics)
- Denny, Luxton-Reilly & Carpenter 2014, "Enhancing syntax error messages appears ineffectual".
  Abstract. [record](https://researchspace.auckland.ac.nz/handle/2292/43268)
- Dunlosky et al. 2013. Summary. [APS release](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)
- Ericson, Margulieux & Rick 2017, Parsons vs fixing and writing code. Summary. [summary](https://hg.gatech.edu/node/603172)
- Erickson, *Algorithms*, "About the Exercises". Full text. [front matter](https://jeffe.web.engr.illinois.edu/teaching/algorithms/book/!!-frontmatter.pdf)
- Expertise reversal effect. Summary. [overview](https://en.wikipedia.org/wiki/Expertise_reversal_effect)
- Fowler et al. 2021, auto-grading plain-English explanations. Abstract. [PDF](https://zilles.web.engr.illinois.edu/papers/fowler_EiPE_NLP_SIGCSE_2021.pdf)
- FSRS. Documentation. [project](https://github.com/open-spaced-repetition/fsrs4anki)
- Götschi, Sanders & Galpin 2003, mental models of recursion. Abstract. [record](https://homepages.inf.ed.ac.uk/vgalpin1/pubs/GSG03.html)
- Hassan et al., replication of the reading/writing hierarchy. Abstract. [record](https://par.nsf.gov/servlets/purl/10340072)
- Hundhausen, Douglas & Stasko 2002, algorithm visualization meta-study. Abstract. [record](https://www.academia.edu/15636659/A_Meta_Study_of_Algorithm_Visualization_Effectiveness)
- Kizilcec et al. 2020, behavioural interventions in online education. Abstract. [PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC7334459)
- Kulik, Kulik & Bangert-Drowns 1990, mastery learning. Abstract. [record](https://www.academia.edu/81783373/Effectiveness_of_Mastery_Learning_Programs_A_Meta_Analysis)
- Loksa et al. 2016, explicit problem-solving instruction. Full text. [PDF](https://faculty.washington.edu/ajko/papers/Loksa2016ProgrammingProblemSolving.pdf)
- Lopez et al. 2008, reading, tracing and writing. Full text. [PDF](https://opus.lib.uts.edu.au/bitstream/10453/10806/1/2008001530.pdf)
- Marwan, Williams & Price 2019, programming hints. Full text. [PDF](https://isnap.csc.ncsu.edu/home/public/papers/MarwanICER2019.pdf)
- Marwan et al. 2023, hints in the classroom. Abstract. [PDF](https://isnap.csc.ncsu.edu/home/public/papers/Marwan2023TLT.pdf)
- Math Academy (Skycak), implicit repetition. Summary. [article](https://justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/)
- MIT 6.006 (Demaine, Ku, Solomon), SRTBOT. Lecture notes. [PDF](https://live.ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/665523227a175e9e9ce26ea8d3e5b51c_MIT6_006S20_lec17.pdf)
- Murphy, Fitzgerald, Lister & McCauley 2012, explaining code vs writing it. Abstract. [record](https://opus.lib.uts.edu.au/handle/10453/22969)
- Naps et al. 2002, visualization and engagement. Abstract. [DOI](https://doi.org/10.1145/960568.782998); mixed later support noted in [RPTEL 2015](https://link.springer.com/article/10.1186/s41039-015-0014-0)
- Pelchen, Mathieson & Lister, learning hierarchy in data-structures exams. Full text. [PDF](https://opus.lib.uts.edu.au/rest/bitstreams/bca157a5-e4ab-4edc-93d8-84f0fceb84ca/retrieve)
- PRIMM. Summary. [overview](https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf)
- Rohrer, Dedrick & Burgess 2014, interleaved practice. Full text. [PDF](https://gwern.net/doc/psychology/spaced-repetition/2014-rohrer.pdf)
- Rohrer & Taylor 2006, overlearning and spacing. Full text. [record](https://digitalcommons.usf.edu/psy_facpub/1770/)
- Sailer & Homner 2020, gamification meta-analysis. Abstract. [paper](https://link.springer.com/article/10.1007/s10648-019-09498-w)
- Sedgewick & Wayne, doubling test. Documentation. [DoublingRatio](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/DoublingRatio.html)
- Settles & Meeder 2016, Duolingo's spacing model. Full text. [PDF](https://aclanthology.org/P16-1174.pdf)
- Shih, Koedinger & Scheines 2008, bottom-out hints. Full text. [PDF](https://www.cmu.edu/dietrich/philosophy/docs/scheines/Shih_Koedinger_Scheines_2008_EDM.pdf)
- Sinha & Kapur 2021, problem solving before instruction. Abstract. [ERIC](https://eric.ed.gov/?id=EJ1308129)
- Sorva 2013, "Notional Machines and Introductory Programming Education", *ACM Transactions on
  Computing Education* 13(2). Not checked.
- UBC CPSC 320, "How to Solve a 320 Problem". Full text. [PDF](https://blogs.ubc.ca/cpsc320/files/2016/09/how-to-solve-320-problems.pdf)
- USACO Guide, Practicing. Full text. [page](https://usaco.guide/general/practicing)
- Weinman, Fox & Hearst 2021, faded Parsons problems. Full text. [PDF](https://acelab.berkeley.edu/wp-content/papercite-data/pdf/parsons-chi2021.pdf)
- Wiedenbeck et al. 2004, self-efficacy and mental models. Full text. [PDF](https://ppig.org/files/2004-PPIG-16th-wiedenbeck.pdf)
- Xie et al. 2019, a theory of instruction for programming. Full text. [PDF](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)
