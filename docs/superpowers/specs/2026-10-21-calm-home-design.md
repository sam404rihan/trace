# Calm home: one next step, a roadmap, and a warm illustrated look

Status: reviewed, waiting for approval (2026-10-21). Product truth: `PRODUCT.md`.

## Why

Trace opens on a page that shows everything at once: a headline, a stats row, three study plans,
all 34 topics in six stages, a review section and a footer. The sidebar lists the same 34 topics
again. The person who built it put it plainly: "OVERLOAD OF INFO, too many problems worried". A
beginner who feels worried stops. They asked for a UI that is uncluttered ("free"), beginner
friendly and appealing, that lets them "start where I last stopped", with colour and style "like
Brilliant", "or even a roadmap".

## What they chose (brainstorm, 2026-10-21)

- **Home direction C, "just the next step":** almost nothing on screen; the next thing to do, how
  far along you are, one button. The roadmap is one tap away.
- **Style C3, "warm and illustrated, like Brilliant":** friendly colours and rounded shapes, with a
  drawing of the actual data structure (a tree, an array with pointers, a graph) as the main
  picture. They rejected looks that "don't look like an app for DSA".
- Mockups: `.superpowers/brainstorm/591-1792576376/content/home-direction.html` (option C) and
  `next-step-style.html` (option C3).

## Goals

1. **Home shows one next step.** A large drawing of the data structure the current topic is about,
   the topic name, the next item's title and kind, one primary button, a small progress line, and
   a link to the roadmap. Nothing else above the fold, and nothing long below it.
2. **Continue resumes where you stopped.** The button opens the last thing you worked in, if it
   isn't finished; otherwise the next unfinished item in course order (today's `nextUp()`).
   - "Worked in" means a problem, intuition drill or walkthrough page that actually opened. A lock
     screen you backed away from doesn't count; "Open anyway" does. The review drill doesn't count
     (it isn't a place on the path). *(My call.)*
   - Study-plan problems count, and Continue reopens them inside the plan (the plan's arrows, no
     ladder locks). *(Their decision, 2026-10-21.)* The hero then says which plan it's from.
   - Finished means: a problem is solved, a walkthrough has all its layers, a drill is solid
     (`T.DrillProgress.solid`). *(My call.)*
3. **A roadmap page** (`#/roadmap`) holds the full course: six stages as a path, the current stage
   open with its topics, the other stages folded to one compact line each whose topics are still
   small numbered links, so every topic is two clicks from home. Study plans, the review drill,
   the starting check and "Reset all progress" move here (or one level under it), so nothing is
   lost.
4. **A new visual world** across the whole app (see below), in light and dark.
5. **A quieter sidebar:** Home, Roadmap, Study plans, search, and the current stage's topics only,
   instead of all 34.

## Non-goals (this round)

- Restructuring the topic page, the problem workspace, the drill pages or the starting check.
  They get the new look through shared tokens and components only. Calming their layouts is a
  later round.
- New course content, new features, accounts, sync, streaks or gamification.
- Changing routes other than adding `#/roadmap`. Every existing link keeps working.

## Anti-goals (fail even if it works)

- Home still shows lists, stats or more than one call to action competing with Continue.
- Anything removed rather than tucked away: plans, the review drill, the starting check, reset,
  search and every topic must stay reachable within two clicks of home.
- Decoration that isn't the subject: stock icon tiles, gradients or blobs in place of a drawing
  of the real data structure.
- A look that reads as a generic "cosy" app (cream paper, serif headings, lamplight) rather than
  a bright, confident learning app about code.

## The visual world (C3, committed)

- **Ground and colour.** A clean light ground with bright, saturated colour fields that own whole
  regions (the home hero is painted in its stage's colour, not a colour accent on white). Each of
  the six stages has its own colour, used on home, the roadmap and as the accent on that stage's
  pages. Green stays "passed", orange-red stays "failed". A full dark rendition with the same
  stage colours, deepened.
- **Shapes.** Generous rounding, chunky tactile buttons (a darker bottom edge that presses down
  on click), soft filled surfaces instead of hairline boxes.
- **Type.** Keep the vendored faces so the app stays offline: Schibsted Grotesk for text, in
  heavier weights for headings; IBM Plex Mono for code only. *(My call: no new font downloads.)*
- **The drawings.** Each topic gets a hero illustration drawn in SVG by code from a small set of
  primitives: array with pointers or a window bracket, linked nodes, tree, heap, trie, graph,
  grid, stack, queue, bit row, number line, points and hull, curves. 34 topics map onto these
  (for example: Two pointers = array with L and R; Sliding window = array with a bracket; Trees =
  a binary tree; Network flow = a small graph with capacities). They use the stage colour plus
  one or two partner colours and real-looking values. *(My call: drawn in code, no image files,
  so they scale, theme and stay small.)*
- **Motion.** One orchestrated moment on home: the drawing builds in (nodes and edges appear in
  order) when the page opens, and settles. Respect `prefers-reduced-motion`. No scattered hover
  effects.

## Home in detail

- Hero card in the stage colour: the topic drawing on one side, and on the other an eyebrow
  ("Stage 2 · Core patterns"), the topic name, the next item's title with its kind ("Guided
  problem", "Intuition drill", "Read the code"), and the button: "Start" if nothing in the course
  is done yet, otherwise "Continue".
- Under the hero: one progress line for the topic ("4 of 12 in Two pointers"), and the link "See
  the roadmap".
- First visit (nothing done, no starting check) still redirects to "Where are you starting?" as
  today. A learner who skipped it sees a quiet "Not sure where to start? Take the starting check"
  link under the hero; once they've placed, it goes away from home and lives on the roadmap.
- Everything done: the hero celebrates the finished course and points to the review drill and
  the study plans.

## Which topic is "current"

- The **hero** shows the topic of whatever Continue will open (so a Blind 75 problem from Stage 5
  shows that topic's drawing, labelled with the plan).
- The **roadmap and sidebar** show your place on the course path, the topic of `nextUp()`, marked
  "You're here". *(My call: a detour into a plan shouldn't move your place on the path.)*
- A page's **accent colour** is the stage of the page being viewed.

## Roadmap in detail

- Six stages top to bottom as a path. Finished stages show a check, the current one is open and
  shows its topics as stops on the path (done, current, ahead; placed-out topics marked), other
  stages are folded to their name, progress and a compact row of numbered topic links, and open
  fully on click.
- Each topic stop links to its topic page and shows a small progress count.
- Below the path: Study plans (as today's rows), Review (as today's row, including its locked
  state), then the starting check link and "Reset all progress".

## Constraints

- Vanilla JS, HTML and CSS in `web/`; no build step, no new dependencies, no network at runtime.
- Keep keyboard and screen-reader behaviour: real links and buttons, visible focus, headings in
  order, drawings `aria-hidden` with the topic named in text.
- Works at phone width (the app already collapses the sidebar under 900px).
- `prefers-color-scheme` and the theme toggle keep working.
- Existing browser checks that assert on home (`scratchpad/cdp/t5`, `t5b`, `t7`, `t8`) are updated
  to the new markup; the repo's `tests/browser/*.mjs` keep passing.

## Left to the builder

- Exact colour values, sizes and spacing, within the world above.
- How each topic maps to a drawing primitive and what values it shows.
- How "last stopped" is stored (local storage is fine; it's per machine, like the theme).
- Exact wording of small labels, in the course's existing plain voice.
