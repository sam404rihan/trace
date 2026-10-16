import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402
from technique_coverage import check_coverage  # noqa: E402

TECH = {"t.x": {"name": "X", "explain": "x"}, "t.y": {"name": "Y", "explain": "y"}}


def course(*topics):
    """topics: (topic_id, [(name, kind, difficulty, uses, teaches), ...]) in course order."""
    tl, probs = [], {}
    for tid, items in topics:
        tl.append({"id": tid, "items": [i[0] for i in items]})
        for name, kind, diff, uses, teaches in items:
            probs[name] = {"kind": kind, "difficulty": diff, "uses": uses, "teaches": teaches,
                           "audited": True, "topic_id": tid}
    return tl, probs


GOOD = course(("01_a", [("snip", "snippet", "", [], ["t.x"]), ("teach_y", "solo", "easy", ["t.x"], ["t.y"]),
                        ("user", "solo", "medium", ["t.x", "t.y"], [])]),
              ("02_b", [("later", "solo", "hard", ["t.y"], [])]))


def run(c, tech=TECH):
    return check_coverage(c[0], c[1], tech)


class Rules(unittest.TestCase):
    def test_good_course_passes(self):
        self.assertEqual(run(GOOD), ([], []))

    def test_unknown_id(self):
        c = course(("01_a", [("p", "solo", "easy", ["t.zzz"], ["t.x", "t.y"])]))
        self.assertTrue(any("t.zzz" in e and "techniques.py" in e for e in run(c)[0]))

    def test_technique_without_teacher(self):
        c = course(("01_a", [("p", "solo", "easy", [], ["t.x"])]))
        self.assertTrue(any(e.startswith("t.y: no problem teaches it") for e in run(c)[0]))

    def test_two_teachers(self):
        c = course(("01_a", [("p", "solo", "easy", [], ["t.x", "t.y"]), ("q", "snippet", "", [], ["t.x"])]))
        self.assertTrue(any(e.startswith("t.x: taught by") for e in run(c)[0]))

    def test_teacher_must_be_basic(self):
        c = course(("01_a", [("p", "solo", "medium", [], ["t.x", "t.y"])]))
        self.assertTrue(any("p: teaches t.x" in e and "medium" in e for e in run(c)[0]))

    def test_teacher_later_in_same_topic(self):
        c = course(("01_a", [("snip", "snippet", "", ["t.x"], ["t.y"]), ("teach", "solo", "easy", [], ["t.x"])]))
        self.assertIn("snip uses t.x, but its teacher teach comes later in the same topic", run(c)[0])

    def test_teacher_in_later_topic(self):
        c = course(("01_a", [("p", "solo", "hard", ["t.x"], []), ("t", "snippet", "", [], ["t.y"])]),
                   ("02_b", [("q", "snippet", "", [], ["t.x"])]))
        self.assertIn("p uses t.x, but its teacher q comes in a later topic", run(c)[0])

    def test_earlier_topic_teacher_is_fine(self):
        self.assertFalse([e for e in run(GOOD)[0] if "later" in e])

    def test_cycle_is_an_error(self):
        c = course(("01_a", [("a", "solo", "easy", ["t.y"], ["t.x"]), ("b", "solo", "easy", ["t.x"], ["t.y"])]))
        self.assertTrue(any("comes later in the same topic" in e for e in run(c)[0]))

    def test_same_id_taught_and_used(self):
        c = course(("01_a", [("p", "solo", "easy", ["t.x"], ["t.x", "t.y"])]))
        self.assertIn("p: t.x is in both TEACHES and USES", run(c)[0])

    def test_tags_must_be_lists_of_ids(self):
        c = course(("01_a", [("p", "solo", "easy", "t.x", ["t.x", "t.y"])]))
        self.assertIn("p: USES must be a list of technique ids", run(c)[0])

    def test_unaudited_is_a_warning_only(self):
        c = course(("01_a", [("snip", "snippet", "", [], ["t.x", "t.y"]), ("old", "solo", "hard", [], [])]))
        c[1]["old"]["audited"] = False
        errors, warnings = run(c)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["old (01_a): not audited yet"])


class RealCourse(unittest.TestCase):
    def test_no_coverage_errors(self):
        topics, problems = server.load_course()
        errors, _ = check_coverage(topics, problems, server.parse_techniques(server.TECHNIQUES_FILE))
        self.assertEqual(errors, [])


class GraphTraversalPilot(unittest.TestCase):
    def setUp(self):
        self.topics, self.problems = server.load_course()
        self.topic = next(t for t in self.topics if t["id"] == "19_graph_traversal")

    def test_every_problem_is_audited(self):
        self.assertEqual([n for n in self.topic["items"] if not self.problems[n]["audited"]], [])

    def test_teachers_come_before_their_users(self):
        items = self.topic["items"]
        for teacher, user in (("flood_fill", "count_enclosed"), ("flood_fill", "num_islands"),
                              ("num_islands", "max_area_island"), ("count_enclosed", "pacific_atlantic"),
                              ("key_then_exit", "shortest_path_all_keys"), ("route_to_exit", "solve_maze")):
            self.assertLess(items.index(teacher), items.index(user), (teacher, user))

    def test_new_basics_are_easy(self):
        for name in ("reachable_nodes", "count_enclosed", "fewest_steps", "key_then_exit", "route_to_exit", "num_islands"):
            self.assertEqual(self.problems[name]["difficulty"], "easy", name)

    def test_every_plan_item_exists(self):
        plans = server.load_plans()["plans"]
        missing = [n for pl in plans for s in pl["sections"] for n in s["items"] if n not in self.problems]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
