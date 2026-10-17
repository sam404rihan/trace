"""
Range Additions                                                               [easy]

Start with n zeros. Each update [l, r, v] adds v to every index from l to r,
both ends included. Return the list after all the updates.

Example:
    range_additions(5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]])  ->  [-2, 0, 3, 5, 3]

Aim for:  O(n + updates). The last test has 100,000 indexes and 50,000 updates
          that each cover much of the list: adding v one index at a time times out.
Hint:     Keep a list diff of n + 1 zeros. An update only touches its two ends:
          diff[l] += v and diff[r + 1] -= v. At the end, the running total of diff
          up to each index is that index's value.
"""


def range_additions(n: int, updates: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["prefix.difference"]
USES = ["prefix.sums"]

TESTS = [
    ((5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]]), [-2, 0, 3, 5, 3]),
    ((3, []), [0, 0, 0]),
    ((1, [[0, 0, 7]]), [7]),
    ((4, [[0, 3, 1], [0, 3, 1]]), [2, 2, 2, 2]),
    ((6, [[2, 2, 5], [0, 5, -1], [3, 5, 4]]), [-1, -1, 4, 3, 3, 3]),
    ((100_000, [[i, 99_999 - i, 1] for i in range(50_000)]), [min(i, 99_999 - i) + 1 for i in range(100_000)]),
]
