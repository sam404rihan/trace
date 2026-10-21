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

These aren't part of `python -m unittest`; run them when you change a screen.
