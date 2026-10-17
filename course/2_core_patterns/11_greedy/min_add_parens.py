"""
Minimum Add to Make Parentheses Valid                                         [easy]

`s` holds only "(" and ")". Return the fewest brackets you must add, anywhere,
so that every bracket is matched: each "(" is closed by a later ")".

Example:
    min_add_parens("())")     ->  1      add a "(" at the front
    min_add_parens("(((")     ->  3
    min_add_parens("()))((")  ->  4

Aim for:  O(n). The last test has 400,000 brackets: deleting "()" pairs over and
          over until none are left is O(n²) and times out.
Hint:     Walk once keeping open, the number of "(" not closed yet. A "(" adds 1.
          A ")" closes one if open > 0; if open is 0, nothing can close it, so you
          must add a "(" for it. At the end, every bracket still open needs a ")".
"""


def min_add_parens(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["brackets.balance"]
USES = []

TESTS = [
    (("())",), 1),
    (("(((",), 3),
    (("()))((",), 4),
    (("",), 0),
    (("()",), 0),
    ((")(",), 2),
    (("(()())",), 0),
    (("))",), 2),
    (("(" * 200_000 + ")" * 200_000,), 0),
]
