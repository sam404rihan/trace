"""
Largest Number                                                              [medium]

Arrange the non-negative integers in `nums` so that, written one after
another, they form the largest possible number. Return it as a string.

Example:
    largest_number([3, 30, 34, 5, 9])  ->  "9534330"

Aim for:  O(n log n)
Hint:     Sorting by plain string order puts "30" before "3", which is wrong.
          Compare two strings a and b by which is bigger: a + b or b + a.
          functools.cmp_to_key turns that comparison into a sort key.
          Watch out for [0, 0]: the answer is "0", not "00".
"""


def largest_number(nums: list[int]) -> str:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    (([10, 2],), "210"),
    (([3, 30, 34, 5, 9],), "9534330"),
    (([0, 0],), "0"),
    (([1],), "1"),
    (([432, 43243],), "43243432"),
]
