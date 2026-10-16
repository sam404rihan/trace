import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server  # noqa: E402

TOPICS = [{"id": "01_a", "title": "A", "stage_n": 1}, {"id": "06_b", "title": "B", "stage_n": 2},
          {"id": "30_z", "title": "Z", "stage_n": 6}]

GOOD = '''
SKILLS = ("names", "loops", "functions", "lists", "dicts", "objects")
READY = [{"skill": s, "question": "What does this print?", "code": "print(1)", "options": ["1", "2"],
          "answer": 0, "explain": "e", "output": True} for s in SKILLS]
Q = {"question": "q", "options": ["x", "y"], "answer": 1, "explain": "e"}
TOPICS = {"01_a": [Q, dict(Q, code="""
    a = 1
    print(a)
""")], "06_b": [Q, Q]}
'''


def write(tmp, source):
    path = Path(tmp) / "starting_check.py"
    path.write_text(textwrap.dedent(source), encoding="utf-8")
    return path


class ParseStartingCheck(unittest.TestCase):
    def parse(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            return server.parse_starting_check(write(tmp, source), TOPICS)

    def test_parses_stage_1_to_4_in_course_order(self):
        check = self.parse(GOOD)
        self.assertEqual([t["id"] for t in check["topics"]], ["01_a", "06_b"])
        self.assertEqual(check["topics"][0]["questions"][1]["code"], "a = 1\nprint(a)")
        self.assertEqual(check["topics"][0]["questions"][0]["code"], "")
        self.assertEqual([q["skill"] for q in check["ready"]], list(server.SKILLS))
        self.assertTrue(check["ready"][0]["output"])
        self.assertFalse(check["topics"][1]["questions"][0]["output"])

    def test_bad_answer_index_names_the_question(self):
        with self.assertRaisesRegex(ValueError, "01_a question 1"):
            self.parse(GOOD.replace('"answer": 1', '"answer": 7'))

    def test_missing_stage_topic(self):
        with self.assertRaisesRegex(ValueError, "missing: 06_b"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', ''))

    def test_unknown_topic(self):
        with self.assertRaisesRegex(ValueError, "unknown: 99_nope"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q, Q], "99_nope": [Q, Q]'))

    def test_needs_exactly_two_questions(self):
        with self.assertRaisesRegex(ValueError, "06_b: needs exactly two"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q]'))

    def test_ready_needs_one_question_per_skill(self):
        with self.assertRaisesRegex(ValueError, "READY"):
            self.parse(GOOD.replace('"objects")', '"names")'))

    def test_output_question_needs_code(self):
        with self.assertRaisesRegex(ValueError, "06_b question 2"):
            self.parse(GOOD.replace('"06_b": [Q, Q]', '"06_b": [Q, dict(Q, output=True)]'))

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                server.parse_starting_check(Path(tmp) / "starting_check.py", TOPICS)


class Place(unittest.TestCase):
    ORDER = ["01_a", "02_b", "03_c", "04_d"]

    def test_all_right_places_out_everything_asked(self):
        r = server.place("python", {}, {"01_a": [True, True], "02_b": [True, True]}, self.ORDER)
        self.assertEqual(r, {"start": "03_c", "placed_out": ["01_a", "02_b"]})

    def test_a_miss_on_the_first_topic_starts_there(self):
        r = server.place("python", {}, {"01_a": [False], "02_b": [True, True]}, self.ORDER)
        self.assertEqual(r, {"start": "01_a", "placed_out": ["02_b"]})

    def test_topics_never_asked_are_not_placed_out(self):
        r = server.place("python", {}, {"01_a": [True, True], "02_b": [True, False]}, self.ORDER)
        self.assertEqual(r, {"start": "02_b", "placed_out": ["01_a"]})

    def test_stopping_before_any_answer_starts_at_the_beginning(self):
        self.assertEqual(server.place("dsa", {}, {}, self.ORDER), {"start": "01_a", "placed_out": []})

    def test_everything_placed_out_has_no_start(self):
        answers = {t: [True] for t in self.ORDER}
        self.assertEqual(server.place("dsa", {}, answers, self.ORDER), {"start": None, "placed_out": self.ORDER})


class RecordPlacement(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = server.PROGRESS_FILE, server.WORKSPACE
        server.WORKSPACE = Path(self.tmp.name)
        server.PROGRESS_FILE = server.WORKSPACE / "progress.json"

    def tearDown(self):
        server.PROGRESS_FILE, server.WORKSPACE = self.old
        self.tmp.cleanup()

    def test_not_taken_by_default(self):
        self.assertIsNone(server.load_progress()["placement"])

    def test_stores_door_date_and_result(self):
        p = server.record_placement("python", {"names": True},
                                    {"01_big_o_in_practice": [True, True], "02_python_toolkit": [False]})["placement"]
        self.assertEqual(p["door"], "python")
        self.assertEqual(p["ready"], {"names": True})
        self.assertEqual(p["placed_out"], ["01_big_o_in_practice"])
        self.assertEqual(p["start"], "02_python_toolkit")
        self.assertRegex(p["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_skip_and_new_store_only_door_and_date(self):
        self.assertEqual(set(server.record_placement("skip")["placement"]), {"door", "date"})
        self.assertEqual(server.record_placement("new")["placement"]["door"], "new")

    def test_retake_replaces_the_old_result(self):
        server.record_placement("dsa", {}, {"01_big_o_in_practice": [True], "12_stacks": [True]})
        p = server.record_placement("python", {}, {"01_big_o_in_practice": [False]})["placement"]
        self.assertEqual((p["door"], p["placed_out"], p["start"]), ("python", [], "01_big_o_in_practice"))

    def test_rejects_bad_input_without_touching_progress(self):
        before = server.load_progress()
        for args in (("expert",), ("python", {"names": "yes"}, {}), ("python", {"swimming": True}, {}),
                     ("python", {}, {"99_nope": [True]}), ("python", {}, {"30_number_theory": [True]}),
                     ("python", {}, {"12_stacks": [True, True, True]}), ("python", {}, {"12_stacks": []}),
                     ("python", {}, {"12_stacks": "true"}), ("python", {}, {"12_stacks": [1]})):
            with self.assertRaises(ValueError, msg=args):
                server.record_placement(*args)
        self.assertEqual(server.load_progress(), before)

    def test_reset_clears_placement(self):
        server.record_placement("skip")
        self.assertIsNone(server.reset_progress()["placement"])


class RealFile(unittest.TestCase):
    def test_course_file_parses(self):
        check = server.parse_starting_check(server.STARTING_CHECK, server.load_course()[0])
        self.assertEqual(len(check["ready"]), 6)
        self.assertEqual(len(check["topics"]), 25)
        self.assertEqual(check["topics"][0]["id"], "01_big_o_in_practice")


if __name__ == "__main__":
    unittest.main()
