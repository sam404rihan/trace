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


if __name__ == "__main__":
    unittest.main()
