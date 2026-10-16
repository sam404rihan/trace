"""
Set Matrix Zeroes                                                             [medium]

If a cell is 0, set its whole row and whole column to 0. Do it IN PLACE and
return nothing. Only zeros that were there at the start spread. Zeros you
write must not spread further.

Example:
    [[1, 1, 1],        [[1, 0, 1],
     [1, 0, 1],   ->    [0, 0, 0],
     [1, 1, 1]]         [1, 0, 1]]

Aim for:  O(1) extra space by using the first row and first column as your markers.
Hint:     The easy way first: collect the zero rows and zero columns in two sets, then
          clear them in a second pass. That's O(m + n) space, and fine to start with.
"""


def set_matrix_zeroes(matrix: list[list[int]]) -> None:
    raise NotImplementedError  # replace this line with your solution


_SEEN = []


def PREPARE(matrix):
    _SEEN[:] = [matrix]
    return (matrix,)


def FINISH(_):
    return _SEEN[0]


def _brute(m):
    rows = {r for r, row in enumerate(m) for v in row if v == 0}
    cols = {c for row in m for c, v in enumerate(row) if v == 0}
    return [[0 if r in rows or c in cols else v for c, v in enumerate(row)] for r, row in enumerate(m)]


def _cases():
    import random
    rng = random.Random(43)
    out = []
    for _ in range(6):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        m = [[0 if rng.random() < 0.15 else rng.randint(1, 9) for _ in range(C)] for _ in range(R)]
        out.append(((m,), _brute(m)))
    return out


USES = ["hash.set_lookup"]

TESTS = [
    (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
    (([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],), [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
    (([[1, 2], [3, 4]],), [[1, 2], [3, 4]]),
    (([[0]],), [[0]]),
] + _cases()
