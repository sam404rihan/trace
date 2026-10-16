import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402

REGISTRY = '''
TECHNIQUES = {
    "bfs.grid": {"name": "BFS on a grid", "explain": "A queue hands out cells in order of distance."},
    "bfs.multi_source": {"name": "Multi-source BFS", "explain": "Start with every source in the queue."},
}
'''


def write(tmp, source, name="techniques.py"):
    path = Path(tmp) / name
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseTechniques(unittest.TestCase):
    def parse(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            return server.parse_techniques(write(tmp, source))

    def test_parses_names_and_explanations(self):
        t = self.parse(REGISTRY)
        self.assertEqual(list(t), ["bfs.grid", "bfs.multi_source"])
        self.assertEqual(t["bfs.grid"], {"name": "BFS on a grid", "explain": "A queue hands out cells in order of distance."})

    def test_bad_id(self):
        with self.assertRaisesRegex(ValueError, "BFS-Grid"):
            self.parse(REGISTRY.replace('"bfs.grid"', '"BFS-Grid"'))

    def test_missing_explain(self):
        with self.assertRaisesRegex(ValueError, "bfs.grid"):
            self.parse(REGISTRY.replace('"explain": "A queue hands out cells in order of distance."', '"explain": ""'))

    def test_python_errors_become_value_errors(self):
        with self.assertRaisesRegex(ValueError, "techniques.py"):
            self.parse(REGISTRY + "\nTECHNIQUES = {oops\n")

    def test_missing_file_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(server.parse_techniques(Path(tmp) / "techniques.py"), {})

    def test_broken_registry_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(server.load_techniques_safely(write(tmp, "TECHNIQUES = 5\n")), {})


PROBLEM = '''
"""
Spread                                                                        [easy]

Statement.
"""


def spread(grid):
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.multi_source"]
USES = ["bfs.grid"]

TESTS = [((["."],), 0)]
'''


class ProblemTags(unittest.TestCase):
    def test_tags_are_read_and_stay_out_of_the_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = server.parse_problem(write(tmp, PROBLEM, "spread.py"))
        self.assertEqual((p["uses"], p["teaches"], p["audited"]), (["bfs.grid"], ["bfs.multi_source"], True))
        self.assertNotIn("USES", p["starter"])
        self.assertNotIn("TEACHES", p["starter"])

    def test_untagged_problem_is_not_audited(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = server.parse_problem(write(tmp, PROBLEM.replace('TEACHES = ["bfs.multi_source"]\nUSES = ["bfs.grid"]\n', ""), "spread.py"))
        self.assertEqual((p["uses"], p["teaches"], p["audited"]), ([], [], False))


def prob(name, rank, title=None, uses=(), teaches=()):
    return {"name": name, "rank": rank, "title": title or name, "uses": list(uses), "teaches": list(teaches)}


class LadderOrder(unittest.TestCase):
    def test_teacher_comes_first_within_a_rank(self):
        found = [prob("a_user", 2, uses=["t.x"]), prob("z_teacher", 2, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["z_teacher", "a_user"])

    def test_rank_still_comes_first(self):
        found = [prob("hard_one", 4), prob("easy_user", 2, uses=["t.x"]), prob("snip", 0, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["snip", "easy_user", "hard_one"])

    def test_chains_sort_in_teaching_order(self):
        found = [prob("c", 2, uses=["t.y"]), prob("b", 2, uses=["t.x"], teaches=["t.y"]), prob("a", 2, teaches=["t.x"])]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["a", "b", "c"])

    def test_cycle_does_not_hang(self):
        found = [prob("a", 2, uses=["t.y"], teaches=["t.x"]), prob("b", 2, uses=["t.x"], teaches=["t.y"])]
        self.assertEqual(sorted(p["name"] for p in server.ladder_order(found)), ["a", "b"])

    def test_bad_tag_types_are_ignored_for_ordering(self):
        found = [prob("a", 2), {**prob("b", 2), "uses": "t.x"}]
        self.assertEqual([p["name"] for p in server.ladder_order(found)], ["a", "b"])


class Summary(unittest.TestCase):
    BASE = {"name": "p", "title": "P", "kind": "solo", "difficulty": "easy", "tests": 1, "topic_id": "t", "steps": []}

    def test_malformed_tags_reach_the_browser_as_empty_lists(self):
        import json
        for bad in ({"bfs.shortest"}, "bfs.shortest", 5, ["ok", 3]):
            s = server.problem_summary({**self.BASE, "uses": bad, "teaches": bad})
            self.assertEqual((s["uses"], s["teaches"]), ([], []), bad)
            json.dumps(s)

    def test_good_tags_pass_through(self):
        s = server.problem_summary({**self.BASE, "uses": ["a.b"], "teaches": ["c.d"]})
        self.assertEqual((s["uses"], s["teaches"]), (["a.b"], ["c.d"]))


class Payload(unittest.TestCase):
    def test_teacher_names(self):
        techniques = {"t.x": {"name": "X", "explain": "x"}, "t.y": {"name": "Y", "explain": "y"}}
        problems = {"p1": {"teaches": ["t.x"]}, "p2": {"teaches": "nope"}}
        self.assertEqual(server.techniques_payload(problems, techniques),
                         {"t.x": {"name": "X", "explain": "x", "teacher": "p1"},
                          "t.y": {"name": "Y", "explain": "y", "teacher": None}})


if __name__ == "__main__":
    unittest.main()
