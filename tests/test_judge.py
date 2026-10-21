"""The judge (runner/judge.py), run the way the server runs it: one fresh process per job."""
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import server  # noqa: E402

PROBLEM = '''
def depth(n):
    raise NotImplementedError

TESTS = [((3,), 3), ((5_000,), 5_000)]
'''


def judge(code):
    job = {"mode": "test", "name": "depth", "problem": PROBLEM, "code": code}
    out = subprocess.run(server._judge_command(), input=json.dumps(job), capture_output=True, text=True,
                         encoding="utf-8", timeout=60).stdout
    return json.loads(out.split("@@DSA_RESULT@@")[-1])


class RecursionLimitTest(unittest.TestCase):
    """Deep tests teach the explicit stack, so a solution can't raise the recursion limit to get past them."""

    def test_raising_the_limit_inside_the_function_is_an_error(self):
        report = judge("import sys\ndef depth(n):\n    sys.setrecursionlimit(10**6)\n    return n\n")
        self.assertIsNone(report["load_error"])
        for test in report["tests"]:
            self.assertEqual(test["status"], "error")
            self.assertIn("setrecursionlimit", test["error"])
            self.assertIn("explicit stack", test["error"])

    def test_raising_the_limit_at_the_top_of_the_file_is_a_load_error(self):
        report = judge("import sys\nsys.setrecursionlimit(10**6)\ndef depth(n):\n    return n\n")
        self.assertIn("setrecursionlimit", report["load_error"])
        self.assertIn("solution.py", report["load_error"])         # points at the learner's own line

    def test_plain_recursion_still_runs_to_the_normal_limit(self):
        report = judge("def depth(n):\n    return 0 if n == 0 else 1 + depth(n - 1)\n")
        self.assertEqual([t["status"] for t in report["tests"]], ["pass", "error"])
        self.assertIn("RecursionError", report["tests"][1]["error"])


# One long call into C (here summing a huge range) holds the GIL, so the judge's own timer can't
# interrupt it: only the server, from outside the process, can stop it.
STUCK_IN_C = "sum(range(10**14))"
SLOW = '''
def slow(n):
    raise NotImplementedError

TESTS = [((1,), 1), ((2,), 2), ((3,), 3), ((4,), 4)]
'''
SLOW_PROBLEM = {"name": "slow", "source": SLOW}


def timed(fn, *args):
    start = time.monotonic()
    value = fn(*args)
    return value, time.monotonic() - start


class TimeLimitTest(unittest.TestCase):
    """A test is stopped near its 2 s limit, and even code the judge can't interrupt is stopped soon after."""

    def test_a_pure_python_loop_times_out_at_the_test_limit(self):
        report = judge("def depth(n):\n    while True:\n        pass\n")
        statuses = [t["status"] for t in report["tests"]]
        self.assertEqual(statuses, ["timeout", "timeout"])
        for test in report["tests"]:
            self.assertLess(test["ms"], 3000)

    def test_a_pure_python_loop_through_the_server(self):
        reply, seconds = timed(server.run_tests, SLOW_PROBLEM, "def slow(n):\n    while True:\n        pass\n")
        self.assertEqual([t["status"] for t in reply["report"]["tests"]], ["timeout", "timeout", "skipped", "skipped"])
        self.assertLess(seconds, 10)

    def test_one_long_builtin_call_is_stopped_and_reported_as_a_timeout(self):
        code = f"def slow(n):\n    if n == 2:\n        {STUCK_IN_C}\n    return n\n"
        reply, seconds = timed(server.run_tests, SLOW_PROBLEM, code)
        self.assertLess(seconds, 15)
        self.assertNotIn("crash", reply)
        tests = reply["report"]["tests"]
        self.assertEqual([t["status"] for t in tests], ["pass", "timeout", "skipped", "skipped"])
        self.assertEqual(tests[0]["got"], "1")                 # finished tests keep their results
        self.assertEqual(tests[1]["call"], "slow(2)")
        self.assertIn("2s", tests[1]["error"])
        self.assertIn("built-in", tests[1]["error"])            # says why the rest didn't run
        self.assertIsNone(reply["report"]["load_error"])

    def test_a_long_builtin_call_while_loading_is_a_load_error(self):
        reply, seconds = timed(server.run_tests, SLOW_PROBLEM, f"print('hi')\n{STUCK_IN_C}\ndef slow(n):\n    return n\n")
        self.assertLess(seconds, 15)
        self.assertIn("to load", reply["report"]["load_error"])
        self.assertEqual(reply["report"]["tests"], [])

    def test_a_long_builtin_call_in_the_custom_call(self):
        reply, seconds = timed(server.run_tests, SLOW_PROBLEM, "def slow(n):\n    return n\n", STUCK_IN_C)
        self.assertLess(seconds, 15)
        report = reply["report"]
        self.assertEqual([t["status"] for t in report["tests"]], ["pass"] * 4)
        self.assertEqual(report["custom"]["expr"], STUCK_IN_C)
        self.assertIn("Still running", report["custom"]["error"])

    def test_a_script_stuck_in_a_builtin_call_is_stopped_and_keeps_its_output(self):
        reply, seconds = timed(server.run_script, f"print('before')\n{STUCK_IN_C}\nprint('after')\n")
        self.assertLess(seconds, 19)
        self.assertIn("before", reply["output"])
        self.assertNotIn("after", reply["output"])
        self.assertNotIn("@@", reply["output"])
        self.assertIn("10 seconds", reply["killed"])

    def test_a_normal_script_is_unchanged(self):
        reply = server.run_script("import sys\nprint('out')\nprint('err', file=sys.stderr)\nprint(1/0)\n")
        self.assertIn("out", reply["output"])
        self.assertIn("err", reply["output"])
        self.assertIn("ZeroDivisionError", reply["output"])
        self.assertNotIn("@@", reply["output"])
        self.assertEqual(reply["exit_code"], 1)
        self.assertIsNone(reply["killed"])


if __name__ == "__main__":
    unittest.main()
