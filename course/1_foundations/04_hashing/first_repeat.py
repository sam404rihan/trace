"""
First repeat                                                                [snippet]

Walk through `items` and return the first value you see for the second time.
Return None if nothing repeats.

Example:
    first_repeat([3, 1, 4, 1, 3])  ->  1      (the second 1 shows up before the second 3)

Aim for:  one pass, O(n).
Hint:     Keep a set of what you've seen. Check before you add.
"""


def first_repeat(items: list):
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["hash.seen_set"]
USES = []

TESTS = [
    (([3, 1, 4, 1, 3],), 1),
    (([1, 2, 3],), None),
    ((["a", "b", "b", "a"],), "b"),
    (([],), None),
    (([7, 7],), 7),
    (([5, 6, 7, 8, 9, 5],), 5),
]
