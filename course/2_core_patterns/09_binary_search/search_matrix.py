"""
Search a 2D Matrix                                                            [medium]

Each row of the matrix is sorted, and every row's first number is bigger than
the previous row's last. Return True if target is in the matrix.

Example:
    search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3)   ->  True
    search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13)  ->  False

Aim for:  O(log(m · n)).
Hint:     Read it as one sorted list of m · n numbers. Index k is matrix[k // n][k % n].
          Then it's an ordinary binary search.
"""


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(54)
    out = []
    for _ in range(8):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        vals = sorted(rng.sample(range(-50, 100), m * n))
        mat = [vals[r * n:(r + 1) * n] for r in range(m)]
        t = rng.choice(vals + [rng.randint(-60, 110)])
        out.append(((mat, t), t in vals))
    return out


M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
TESTS = [((M, 3), True), ((M, 13), False), ((M, 60), True), ((M, 0), False), (([[1]], 1), True)] + _cases()
