"""
Range Sum Query 2D                                                            [medium]

Build a class over a fixed matrix:

    NumMatrix(matrix)
    sum_region(r1, c1, r2, c2)     the sum of the rectangle with corners (r1, c1) and (r2, c2), inclusive

Example:
    m = NumMatrix([[3, 0, 1], [5, 6, 3], [1, 2, 0]])
    m.sum_region(1, 1, 2, 2)  ->  11        6 + 3 + 2 + 0

Aim for:  O(1) per query after O(rows · cols) setup. The last test has 100,000 queries.
Hint:     2D prefix sums: P[r+1][c+1] = M[r][c] + P[r][c+1] + P[r+1][c] - P[r][c].
          Then a rectangle = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
          (inclusion-exclusion: the corner block was subtracted twice).
"""


class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        raise NotImplementedError

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        raise NotImplementedError


CLASS = "NumMatrix"


def _case(rng, R, C, q, fast=False):
    m = [[rng.randint(-9, 9) for _ in range(C)] for _ in range(R)]
    calls, out = [("NumMatrix", m)], [None]
    P = [[0] * (C + 1) for _ in range(R + 1)]
    for r in range(R):
        for c in range(C):
            P[r + 1][c + 1] = m[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
    for _ in range(q):
        r1, r2 = sorted(rng.randrange(R) for _ in range(2))
        c1, c2 = sorted(rng.randrange(C) for _ in range(2))
        calls.append(("sum_region", r1, c1, r2, c2))
        if fast:
            out.append(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])
        else:
            out.append(sum(m[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)))
    return calls, out


def _cases():
    import random
    rng = random.Random(205)
    return [_case(rng, rng.randint(1, 6), rng.randint(1, 6), 10) for _ in range(5)] + [_case(rng, 300, 300, 100_000, fast=True)]


TESTS = [([("NumMatrix", [[3, 0, 1], [5, 6, 3], [1, 2, 0]]), ("sum_region", 1, 1, 2, 2), ("sum_region", 0, 0, 0, 0),
           ("sum_region", 0, 0, 2, 2)], [None, 11, 3, 21])] + _cases()
