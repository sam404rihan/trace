"""
Merge Two Sorted Lists                                                        [easy]

`a` and `b` are both sorted. Return one sorted list that holds every number
from both.

Example:
    merge_sorted([1, 4, 9], [2, 3, 10])  ->  [1, 2, 3, 4, 9, 10]

Aim for:  O(len(a) + len(b)): walk each list once. Don't call sorted(): the point
          is to use the order the lists already have.
Hint:     Keep i in a and j in b. While both have numbers left, append the smaller
          of a[i] and b[j] and move that pointer on. When one list runs out, add
          the rest of the other.
"""


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["pointers.two_sequences"]
USES = []

TESTS = [
    (([1, 4, 9], [2, 3, 10]), [1, 2, 3, 4, 9, 10]),
    (([], [1, 2]), [1, 2]),
    (([5], []), [5]),
    (([], []), []),
    (([1, 1, 3], [1, 2]), [1, 1, 1, 2, 3]),
    (([-3, 0], [-5, -4, 7]), [-5, -4, -3, 0, 7]),
    (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
    ((list(range(0, 400_000, 2)), list(range(1, 400_000, 2))), list(range(400_000))),
]
