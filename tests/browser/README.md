# Browser checks

Headless-Chrome scenarios for the screens the unit tests can't reach. They need Node 22+ (for its
built-in WebSocket) and Chrome; set `CHROME` if it isn't at the default Windows path. Each run
starts Trace on an empty workspace with a fresh browser profile:

    bash tests/browser/fresh.sh 8170 technique_coverage.mjs
    bash tests/browser/fresh.sh 8171 stage_1.mjs
    bash tests/browser/fresh.sh 8172 stage_2.mjs
    bash tests/browser/fresh.sh 8173 stage_3.mjs
    bash tests/browser/fresh.sh 8174 stage_4.mjs
    bash tests/browser/fresh.sh 8175 stage_5.mjs
    bash tests/browser/fresh.sh 8176 stage_6.mjs
    bash tests/browser/fresh.sh 8177 calm_home.mjs
    bash tests/browser/fresh.sh 8180 workspace.mjs
    bash tests/browser/fresh.sh 8183 drills.mjs
    bash tests/browser/fresh.sh 8190 contest.mjs

These aren't part of `python -m unittest`; run them when you change a screen.

`contest.mjs` covers contest mode. Headless Chrome won't grant fullscreen without a real user
gesture, so the check stubs `document.fullscreenElement` and fires `fullscreenchange` to test the
lock, and moves the countdown forward by replacing `Trace.now`.

Two helpers take screenshots for looking at, not checks:

    bash tests/browser/fresh.sh 8178 screens.mjs "$(pwd)/.impeccable/review" home,roadmap,t/06_two_pointers
    bash tests/browser/fresh.sh 8178 drawings.mjs "$(pwd)/.impeccable/review/sheet"

`screens.mjs` captures each named page (without the `#/`, which Git Bash rewrites) at 1440 and 390
wide, light and dark. `drawings.mjs` puts all 34 topic drawings on one sheet per theme.
