"""
Matrix Chain Multiplication                                                   [easy]

Matrix i has dims[i] rows and dims[i + 1] columns, so there are len(dims) - 1
matrices to multiply in a row. Multiplying a p x q matrix by a q x r one costs
p * q * r. The order of the multiplications (where the brackets go) changes the
total cost. Return the smallest total cost.

Example:
    matrix_chain([10, 30, 5, 60])  ->  4500
        (A B) C costs 10*30*5 + 10*5*60 = 4500; A (B C) costs 30*5*60 + 10*30*60 = 27000.

Aim for:  O(n³) with n matrices. Trying every way of placing the brackets is
          exponential, and the last test has 150 matrices.
Hint:     cost[i][j] = cheapest way to multiply matrices i..j into one. The LAST
          multiplication splits them at some k: (i..k) times (k+1..j), which costs
          cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]. Fill
          the table for short runs first, then longer ones.
"""


def matrix_chain(dims: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(dims):
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = min(cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1] for k in range(i, j))
    return cost[0][n - 1]


def _big():
    import random
    rng = random.Random(2401)
    dims = [rng.randint(1, 100) for _ in range(151)]
    return (dims,), _fast(dims)


TEACHES = ["dp.interval"]
USES = []

TESTS = [
    (([10, 30, 5, 60],), 4500),
    (([40, 20, 30, 10, 30],), 26000),
    (([10, 20, 30],), 6000),
    (([5, 10],), 0),
    (([1, 2, 3, 4, 3],), 30),
    (([10, 20, 30, 40, 30],), 30000),
    _big(),
]
