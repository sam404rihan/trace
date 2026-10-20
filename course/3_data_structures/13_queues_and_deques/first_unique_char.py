"""
First Unique Character                                                        [easy]

Return the index of the first character in `s` that appears exactly once,
or -1 if there isn't one.

Example:
    first_unique_char("loveleetcode")  ->  2      "v"

Aim for:  O(n)
Hint:     Two passes: count every character (Counter), then find the first
          one with a count of 1. (A queue version: push new characters and
          pop from the front while the front has repeated. Try both.)
"""


def first_unique_char(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    (("leetcode",), 0),
    (("loveleetcode",), 2),
    (("aabb",), -1),
    (("",), -1),
    (("z",), 0),
]
