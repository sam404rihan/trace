"""
Add Two Numbers                                                               [medium]

Two non-negative numbers are stored as linked lists of digits in REVERSE order
(ones digit first). Return their sum as a list in the same format.

Example:
    2 → 4 → 3   +   5 → 6 → 4     (342 + 465)
    ->  7 → 0 → 8                  (807)

Aim for:  one pass, like adding on paper.
Hint:     Walk both lists together with a carry. Missing digits count as 0. Keep going
          while either list has nodes left OR the carry isn't 0. A dummy head node
          keeps the building code simple.
"""
from helpers import ListNode, build_list, to_list



def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(a, b):
    return build_list(a), build_list(b)


FINISH = to_list


def _digits(n):
    return [int(d) for d in str(n)[::-1]]


def _cases():
    import random
    rng = random.Random(61)
    out = []
    for _ in range(6):
        x, y = rng.randint(0, 10 ** rng.randint(1, 20)), rng.randint(0, 10 ** rng.randint(1, 20))
        out.append(((_digits(x), _digits(y)), _digits(x + y)))
    return out


USES = ["math.carry", "list.dummy"]

TESTS = [(([2, 4, 3], [5, 6, 4]), [7, 0, 8]), (([0], [0]), [0]), (([9, 9, 9, 9], [9, 9]), [8, 9, 0, 0, 1]),
         (([5], [5]), [0, 1])] + _cases()
