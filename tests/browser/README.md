# Browser checks

Headless-Chrome scenarios for the screens the unit tests can't reach. They need Node 22+ (for its
built-in WebSocket) and Chrome; set `CHROME` if it isn't at the default Windows path. Each run
starts Trace on an empty workspace with a fresh browser profile:

    bash tests/browser/fresh.sh 8170 technique_coverage.mjs

These aren't part of `python -m unittest`; run them when you change a screen.
