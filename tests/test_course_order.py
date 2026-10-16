import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class CourseOrder(unittest.TestCase):
    def setUp(self):
        self.topics, self.problems = server.load_course()

    def test_big_o_comes_before_the_toolkit(self):
        self.assertEqual([t["id"] for t in self.topics[:2]], ["01_big_o_in_practice", "02_python_toolkit"])

    def test_problem_names_survive_the_swap(self):
        by_id = {t["id"]: t for t in self.topics}
        self.assertIn("missing_number", by_id["01_big_o_in_practice"]["items"])
        self.assertIn("running_sum", by_id["02_python_toolkit"]["items"])

    def test_topics_know_their_stage_number(self):
        self.assertEqual({t["stage_n"] for t in self.topics}, {1, 2, 3, 4, 5, 6})
        self.assertEqual(next(t for t in self.topics if t["id"] == "12_stacks")["stage_n"], 3)

    def test_big_o_hints_do_not_assume_the_toolkit(self):
        for name, p in self.problems.items():
            if p["topic_id"] == "01_big_o_in_practice":
                self.assertNotIn("Counter", p["hint"], name)


if __name__ == "__main__":
    unittest.main()
