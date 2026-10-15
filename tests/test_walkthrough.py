import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class StripMarkers(unittest.TestCase):
    def test_strips_and_reports(self):
        code, marks = server.strip_markers("a = 1  #@state\nb = 2  # note #@state\nc = 3\nd = 4 #@valid")
        self.assertEqual(code, "a = 1\nb = 2  # note\nc = 3\nd = 4")
        self.assertEqual(marks, {"state": [1, 2], "valid": [4]})

    def test_unmarked_code_is_unchanged(self):
        src = "def f(x):\n    return x  # plain comment\n"
        self.assertEqual(server.strip_markers(src), (src, {}))

    def test_marker_only_at_line_end(self):
        src = 's = "#@state inside"\n'
        self.assertEqual(server.strip_markers(src), (src, {}))


class AddedLines(unittest.TestCase):
    def test_new_and_changed_lines(self):
        self.assertEqual(server.added_lines("a\nb\nc", "a\nx\nb\n\nc\ny"), [2, 6])

    def test_first_layer_is_all_new(self):
        self.assertEqual(server.added_lines("", "a\n\nb"), [1, 3])


GOOD = '''
"""Build it."""
LAYERS = [
    {"title": "One", "why": "w", "code": """
x = 1
print(x)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 1, "explain": "e"}},
    {"title": "Two", "why": "w", "code": """
x = 1
y = 2
print(x)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 0, "explain": "e"}},
    {"title": "Reuse", "why": "w", "reuse": "min_window", "roles": {"state": "S"}, "code": """
z = 3  #@state
print(z)
""", "check": {"question": "q", "options": ["a", "b"], "answer": 0, "explain": "e"}},
]
'''


def write(tmp, source, name="walkthrough.py"):
    path = Path(tmp) / name
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseWalkthrough(unittest.TestCase):
    def test_parses_layers(self):
        with tempfile.TemporaryDirectory() as tmp:
            wt = server.parse_walkthrough(write(tmp, GOOD))
        self.assertEqual(wt["title"], "Build it.")
        one, two, reuse = wt["layers"]
        self.assertEqual(one["code"], "x = 1\nprint(x)")
        self.assertEqual(one["added"], [1, 2])
        self.assertEqual(two["added"], [2])
        self.assertEqual(reuse["added"], [])
        self.assertEqual(reuse["marks"], {"state": [1]})
        self.assertEqual(reuse["code"], "z = 3\nprint(z)")
        self.assertEqual(reuse["reuse"], "min_window")

    def test_bad_answer_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "layer 1"):
                server.parse_walkthrough(write(tmp, GOOD.replace('"answer": 1', '"answer": 5')))

    def test_unknown_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "valid"):
                server.parse_walkthrough(write(tmp, GOOD.replace("#@state", "#@valid")))

    def test_real_sliding_window(self):
        path = next(server.COURSE.glob("*/07_sliding_window/walkthrough.py"))
        wt = server.parse_walkthrough(path)
        self.assertGreaterEqual(len(wt["layers"]), 5)
        self.assertEqual(wt["layers"][-1]["reuse"], "min_window")
        self.assertEqual(set(wt["layers"][-1]["marks"]), {"state", "valid", "answer"})
        self.assertNotIn("#@", "".join(layer["code"] for layer in wt["layers"]))


class CourseIntegration(unittest.TestCase):
    def test_topic_exposes_walkthrough(self):
        topics, problems = server.load_course()
        topic = next(t for t in topics if t["id"] == "07_sliding_window")
        self.assertTrue(topic["walkthrough"])
        self.assertNotIn("walkthrough", topic["items"])

    def test_broken_walkthrough_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, GOOD.replace('"answer": 1', '"answer": 9'))
            self.assertIsNone(server.load_walkthrough_safely(path))


class Progress(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = server.PROGRESS_FILE, server.WORKSPACE
        server.WORKSPACE = Path(self.tmp.name)
        server.PROGRESS_FILE = server.WORKSPACE / "progress.json"

    def tearDown(self):
        server.PROGRESS_FILE, server.WORKSPACE = self.old
        self.tmp.cleanup()

    def test_walkthrough_progress_is_max_and_validated(self):
        self.assertEqual(server.record_walkthrough("t", 3, 5)["walkthroughs"], {"t": 3})
        self.assertEqual(server.record_walkthrough("t", 1, 5)["walkthroughs"], {"t": 3})
        for bad in (-1, 6, "2", True):
            with self.assertRaises(ValueError):
                server.record_walkthrough("t", bad, 5)


class SolutionSkeleton(unittest.TestCase):
    def test_marked_solution(self):
        code, marks = server.strip_markers((server.SOLUTIONS / "longest_k_distinct.py").read_text(encoding="utf-8"))
        self.assertTrue(marks.get("skeleton"))
        self.assertNotIn("#@", code)


if __name__ == "__main__":
    unittest.main()
