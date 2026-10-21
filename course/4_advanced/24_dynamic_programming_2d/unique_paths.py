"""
Unique Paths                                                                [medium]

A robot starts at the top-left of an m × n grid and can only move right or
down. How many different paths reach the bottom-right corner?

Example:
    unique_paths(3, 7)  ->  28

Aim for:  O(m · n). The last test (18 × 18) has over 2 billion paths, so
          counting them one by one with plain recursion will time out.
Hint:     paths[r][c] = paths[r - 1][c] + paths[r][c - 1]. The top row and
          left column are all 1. (One row is enough: row[c] += row[c - 1].)
"""


def unique_paths(m: int, n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["dp.grid"]

TESTS = [
    ((3, 7), 28),
    ((3, 2), 3),
    ((1, 1), 1),
    ((1, 10), 1),
    ((18, 18), 2333606220),
]
