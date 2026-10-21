"""The judge (runner/judge.py), run the way the server runs it: one fresh process per job."""
import json
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
