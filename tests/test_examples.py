"""A problem's first tests and its parameters, sent to the page so it can draw the inputs."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import server  # noqa: E402


class ProblemExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problems = server.load_course()[1]

    def test_params_carry_names_and_types(self):
        self.assertEqual(self.problems["max_depth"]["params"], [{"name": "root", "type": "TreeNode | None"}])
        self.assertEqual(self.problems["course_schedule"]["params"],
                         [{"name": "num_courses", "type": "int"}, {"name": "prerequisites", "type": "list[list[int]]"}])

    def test_examples_are_the_first_small_tests_as_json(self):
        self.assertEqual(self.problems["max_depth"]["examples"][0],
                         {"args": [[3, 9, 20, None, None, 15, 7]], "expected": 3})
        self.assertEqual(self.problems["course_schedule"]["examples"][0], {"args": [2, [[1, 0]]], "expected": True})
        self.assertLessEqual(len(self.problems["two_sum"]["examples"]), 3)

    def test_guided_problems_use_their_first_step(self):
        self.assertEqual(self.problems["count_pairs_below"]["examples"][0], {"args": [[1, 2, 3, 4], 6], "expected": 4})

    def test_tuples_become_lists_and_big_inputs_are_left_out(self):
        def no_tuples(v):
            return not isinstance(v, tuple) and (not isinstance(v, (list, dict)) or
                                                 all(no_tuples(x) for x in (v.values() if isinstance(v, dict) else v)))
        for p in self.problems.values():
            for ex in p["examples"]:
                self.assertLessEqual(len(repr(ex["args"])), 400, p["name"])
                self.assertTrue(no_tuples(ex), p["name"])

    def test_class_problems_have_no_examples(self):
        self.assertEqual(self.problems["lru_cache"]["examples"], [])
        self.assertEqual(self.problems["lru_cache"]["params"], [])

    def test_the_problem_api_sends_them(self):
        data = server.public_problem(self.problems["max_depth"])
        self.assertNotIn("examples", data)              # the course list stays small; /api/problem adds them


if __name__ == "__main__":
    unittest.main()
