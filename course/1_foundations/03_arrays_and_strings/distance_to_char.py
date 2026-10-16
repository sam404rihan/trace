"""
Shortest Distance to a Letter                                                 [easy]

For every index i of `s`, find how far it is to the nearest copy of the letter
`c`, and return those distances as a list. `c` appears in `s` at least once.

Example:
    distance_to_char("loveleetcode", "e")  ->  [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]

Aim for:  O(n): one pass from the left and one from the right. Searching outwards
          from every index is O(n²) on the big test.
Hint:     Left to right, remember where you last saw c and write i - last (use a big
          number before the first c). Then right to left, remember the last c from
          that side and keep the smaller of the two distances.
"""


def distance_to_char(s: str, c: str) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["array.left_right_passes"]
USES = []

TESTS = [
    (("loveleetcode", "e"), [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]),
    (("aaab", "b"), [3, 2, 1, 0]),
    (("a", "a"), [0]),
    (("baab", "b"), [0, 1, 1, 0]),
    (("abcde", "c"), [2, 1, 0, 1, 2]),
    (("cxxxxc", "c"), [0, 1, 2, 2, 1, 0]),
    (("c" + "x" * 99_998 + "c", "c"), [min(i, 99_999 - i) for i in range(100_000)]),
    (("x" * 50_000 + "c" * 50_000, "c"), [50_000 - i for i in range(50_000)] + [0] * 50_000),
]
