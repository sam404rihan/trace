"""
Rotate Image                                                                  [medium]

Rotate an n×n matrix 90 degrees clockwise, IN PLACE: change `matrix` itself and
return nothing. Making a rotated copy doesn't count.

Example:
    [[1, 2, 3],          [[7, 4, 1],
     [4, 5, 6],    ->     [8, 5, 2],
     [7, 8, 9]]           [9, 6, 3]]

The tests show your matrix as it is after the call.

Aim for:  O(1) extra space.
Hint:     Clockwise rotation = transpose (swap matrix[i][j] with matrix[j][i] for j > i),
          then reverse every row.
"""


def rotate_image(matrix: list[list[int]]) -> None:
    raise NotImplementedError  # replace this line with your solution


_SEEN = []


def PREPARE(matrix):
    _SEEN[:] = [matrix]
    return (matrix,)


def FINISH(_):
    return _SEEN[0]


def _cases():
    import random
    rng = random.Random(42)
    out = []
    for n in (5, 6, 7):
        m = [[rng.randint(-9, 99) for _ in range(n)] for _ in range(n)]
        out.append(((m,), [list(row) for row in zip(*m[::-1])]))
    return out


USES = []

TESTS = [
    (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
    (([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],),
     [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]),
    (([[1]],), [[1]]),
    (([[1, 2], [3, 4]],), [[3, 1], [4, 2]]),
] + _cases()
