#!/usr/bin/env bash
# fresh.sh PORT SCENARIO.mjs: start Trace on an empty workspace, run a scenario against it, stop it.
PORT=$1; shift
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
WS="$(python -c 'import tempfile; print(tempfile.mkdtemp())')"
cd "$ROOT"
TRACE_WORKSPACE="$WS" python server.py --no-browser --port "$PORT" > "$WS/server.log" 2>&1 &
SERVER=$!
for i in $(seq 1 120); do curl -s "localhost:$PORT/api/docker" > /dev/null && break; sleep 1; done
cd "$HERE"
node "$@" "http://localhost:$PORT"
CODE=$?
kill $SERVER 2>/dev/null
exit $CODE
