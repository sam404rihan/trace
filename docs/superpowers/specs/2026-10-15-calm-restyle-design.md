# Calm and clean restyle

**Status:** approved in conversation 2026-10-15 (style "C" from the visual companion).
**Scope:** visual style only. No page layout, routing or behaviour changes.

## Goal

Make Trace feel cleaner and more focused on the content, in the spirit of Brilliant's lesson
screens but without the playfulness: big readable type, soft filled surfaces instead of
borders, one accent colour, clear right/wrong feedback, a visible sense of progress.

## Decisions

### Type
- Keep Schibsted Grotesk (UI and prose) and IBM Plex Mono (code). Both are already vendored
  in `web/vendor/fonts`, so the desktop app stays offline.
- Learning pages (home, topic, drill, walkthrough): body 16.5px / 1.6; lesson and walkthrough
  prose 17px / 1.65; page `h1` ~40px, letter-spacing -0.03em; section and rung headings scale up
  to match.
- Workspace (problem page): body 15px; problem statement 15.5px. Editor font size unchanged.

### Surfaces
- New surface token `--fill` (light `#f6f7fb`, dark `#1b1c22`) for cards, problem rows, drill
  chips, answer choices, facts box, cheat sheet and code blocks.
- Borders are removed from those components. Lines (`--line`) remain only for structure: the
  top bar's bottom edge and the workspace pane splits.
- `--radius` 8px → 12px for cards and blocks; buttons become pills (`border-radius: 999px`).
- Hover on filled items darkens the fill slightly (`--fill-2`).

### Colour
- One accent: light `#4f5fe0`, dark `#8e9bff`, with `--accent-soft` tints. It marks primary
  actions, progress, the current rung and links.
- `.btn.primary` (was ink black) and `.btn.run` (was green) both become accent pills. Green
  (`--ok`) is used only for passed/correct; orange-red (`--bad`) only for failed/wrong.
- Content colours used inside drill boards (`--mark*`, `--pa..--pd`) and the `.board` grid are
  unchanged: they carry meaning in the drills.

### Feedback and progress
- Drill answer choices: soft filled blocks; correct → `--ok-soft` fill with an inset 1.5px
  `--ok` ring; wrong → `--bad-soft` with a `--bad` ring. The explanation line under the
  question uses the matching ink colour.
- Drill pages (and the walkthrough, see the Read-step spec) get a thin 4px progress bar at the
  top of the content: accent on a `--fill` track. For drills it shows question i of n.

### Dark mode
- Every new token gets a dark value in both existing dark blocks
  (`prefers-color-scheme` guarded by `:root:not([data-theme="light"])`, and
  `:root[data-theme="dark"]`).

## Implementation notes
- Almost all work is in `web/app.css`: add tokens, then rewrite component rules to use them.
- `web/drill.js` gains the progress bar element (it already knows the question index via
  `ctx`/the generator loop). No other JS changes are expected.
- Nothing in `server.py` changes.

## Verification
- Run the app (`python server.py`) and look at: home, a topic page, a drill mid-question
  (right and wrong answer), a problem workspace with passing and failing tests, the solution
  tab, and the cheat sheet. Check each in light and dark mode, and at phone width.
- `node --check` on touched JS files.

## Out of scope
- Layout changes, new fonts, animations beyond existing ones, the CodeMirror theme.
