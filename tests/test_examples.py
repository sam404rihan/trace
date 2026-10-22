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

    def ex(self, name, k=0):
        return {key: v for key, v in self.problems[name]["examples"][k].items() if key in ("args", "expected", "note", "source")}

    def test_examples_come_from_the_statement_with_their_notes(self):
        self.assertEqual(self.ex("course_schedule", 0),
                         {"args": [2, [[1, 0]]], "expected": True, "note": "take 0, then 1", "source": "statement"})
        self.assertEqual(self.ex("course_schedule", 1),
                         {"args": [2, [[1, 0], [0, 1]]], "expected": False, "note": "each needs the other first", "source": "statement"})
        self.assertLessEqual(len(self.problems["two_sum"]["examples"]), 3)

    def test_a_call_written_over_several_lines(self):
        self.assertEqual(self.ex("spiral_order")["args"], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]])
        self.assertEqual(self.ex("spiral_order")["expected"], [1, 2, 3, 6, 9, 8, 7, 4, 5])

    def test_a_named_argument_drawn_in_text_comes_from_the_matching_test(self):
        self.assertEqual(self.ex("num_islands"), {"args": [[[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]]],
                                                  "expected": 3, "note": "", "source": "statement"})
        self.assertEqual(self.ex("max_depth")["args"], [[3, 9, 20, None, None, 15, 7]])

    def test_no_call_in_the_statement_falls_back_to_the_first_test(self):
        self.assertEqual(self.ex("rotate_image"), {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]],
                                                   "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]], "note": "", "source": "tests"})

    def test_guided_problems_use_their_first_step(self):
        self.assertEqual(self.ex("count_pairs_below")["args"], [[1, 2, 3, 4], 6])

    def test_return_types_are_recorded(self):
        self.assertEqual(self.problems["max_depth"]["returns"], "int")
        self.assertEqual(self.problems["rotate_image"]["returns"], "None")

    def test_every_test_run_carries_its_inputs(self):
        args = server.case_args(self.problems["course_schedule"], None)
        self.assertEqual(args[0], [2, [[1, 0]]])
        self.assertEqual(len(args), self.problems["course_schedule"]["tests"])
        self.assertTrue(all(a is None or len(repr(a)) <= 400 for a in args))
        self.assertEqual(server.case_args(self.problems["lru_cache"], None), [])

    def test_tuples_become_lists_and_big_inputs_are_left_out(self):
        def no_tuples(v):
            return not isinstance(v, tuple) and (not isinstance(v, (list, dict)) or
                                                 all(no_tuples(x) for x in (v.values() if isinstance(v, dict) else v)))
        for p in self.problems.values():
            for ex in p["examples"]:
                self.assertLessEqual(len(repr(ex["args"])), 400, p["name"])
                self.assertIn(ex["source"], ("statement", "tests"), p["name"])
                self.assertTrue(no_tuples(ex), p["name"])

    def test_class_problems_have_no_examples(self):
        self.assertEqual(self.problems["lru_cache"]["examples"], [])
        self.assertEqual(self.problems["lru_cache"]["params"], [])

    def test_the_problem_api_sends_them(self):
        data = server.public_problem(self.problems["max_depth"])
        self.assertNotIn("examples", data)              # the course list stays small; /api/problem adds them


if __name__ == "__main__":
    unittest.main()
