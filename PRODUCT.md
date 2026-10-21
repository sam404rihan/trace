# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Beginners learning data structures and algorithms, usually on their own and often preparing for
coding interviews. Many are new to DSA or to programming. The person who built Trace uses it
themselves and wants to share it with other beginners.

What they feel today: overwhelmed. Seeing hundreds of problems and a lot of information at once
makes them worried rather than motivated. The job they come to do is "pick up where I left off
and make progress", not "browse a catalogue".

## Product Purpose

Trace teaches DSA in two passes, first in your head and then in code. Each of its 34 topics (in 6
stages) is a ladder: Intuition drills, Snippet, Guided, Problems, Build. It has 415 coding
exercises and 71 drills, a first-run placement check, and study plans (Blind 75, NeetCode 150,
Beyond NeetCode) that cut across the topics.

Success: a beginner opens Trace, sees one clear next step, and keeps coming back because it feels
calm and doable.

## Positioning

Every problem is tagged with the named techniques it teaches and uses (117 techniques), and each
technique is taught before any problem needs it, so Trace knows what a learner has actually
learned and can always say what comes next. Code is checked by a local judge with time limits
that reject the brute-force answer. It runs entirely offline, with nothing to sign up for.

## Operating Context

- Runs on the learner's own machine: a Windows desktop app (Edge WebView2 window with its own
  bundled Python 3.14), or `python server.py` in a browser. Works offline.
- Progress is kept locally; there are no accounts.
- A session is usually: open the app, continue the current topic's next rung or problem, write
  and run code in the built-in editor, read hints or the reference solution when stuck.

## Capabilities and Constraints

- Front end is vanilla JS, HTML and CSS in `web/` with no build step; the server is Python
  standard library (`server.py`).
- Everything ships with the app: fonts are vendored in `web/vendor/fonts`, the editor is
  CodeMirror in `web/vendor/codemirror`. No CDN or network resources at runtime.
- Nothing is removed in the redesign. The full problem list, study plans, the placement check
  and stats stay reachable; they are tucked away, not deleted.
- Terminology already in use: topic, stage, rung (Intuition, Snippet, Guided, Problems, Build),
  drill, technique, study plan, placement check, "Open anyway".

## Brand Commitments

- Name: Trace.
- The user asked for the UI to be uncluttered ("free"), beginner friendly and appealing, and
  chose a warm, illustrated, Brilliant-like direction where a drawing of the actual data
  structure is the main picture (brainstorm choice "C3", 2026-10-21).

## Evidence on Hand

- Real course content: `course/` (lessons, problems, techniques), `web/topics/*.js` (drills).
- No testimonials, user counts or reviews exist. Don't invent any.

## Product Principles

1. One next step at a time. The home screen answers "what do I do now?" and little else.
2. Tuck away, never remove. Depth stays one tap away for those who want it.
3. Calm over complete. When in doubt, show less; a worried beginner stops.
4. Show the structure. Arrays, trees and graphs are drawn, not only described.
5. Free means uncluttered: room to breathe, nothing competing for attention.
