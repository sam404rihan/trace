"""
Number of Submatrices That Sum to Target                                      [hard]

Count the non-empty rectangular submatrices of `matrix` whose values add up to
`target`. Values can be negative. Two submatrices are different if any of
their corners differ.

Example:
    submatrix_sum_target([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], 0)        ->  4      the four single 0s
    submatrix_sum_target([[1, -1],
                          [-1, 1]], 0)          ->  5

Aim for:  O(rows² * cols) for the big test (60 x 60).
Hint:     Fix a top row and a bottom row. Squash the rows between them into one list of column
          sums. Now it's "count subarrays that sum to target" in 1D: walk with a running sum and
          a Counter of earlier prefix sums, adding seen[running - target] at each step.
"""


def submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(matrix, target):
    r, c = len(matrix), len(matrix[0])
    total = 0
    for top in range(r):
        for bottom in range(top, r):
            for left in range(c):
                for right in range(left, c):
                    s = sum(matrix[i][j] for i in range(top, bottom + 1) for j in range(left, right + 1))
                    total += s == target
    return total


def _fast(matrix, target):
    r, c = len(matrix), len(matrix[0])
    total = 0
    for top in range(r):
        col = [0] * c
        for bottom in range(top, r):
            for j in range(c):
                col[j] += matrix[bottom][j]
            seen, running = {0: 1}, 0
            for v in col:
                running += v
                total += seen.get(running - target, 0)
                seen[running] = seen.get(running, 0) + 1
    return total


def _cases():
    import random
    rng = random.Random(1074)
    out = []
    for _ in range(7):
        m = [[rng.randint(-2, 2) for _ in range(rng.randint(1, 4))]]
        m += [[rng.randint(-2, 2) for _ in m[0]] for _ in range(rng.randint(0, 3))]
        t = rng.randint(-2, 2)
        out.append(((m, t), _brute(m, t)))
    big = [[rng.randint(-3, 3) for _ in range(60)] for _ in range(60)]
    out.append(((big, 2), _fast(big, 2)))
    return out


TESTS = [
    (([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 0), 4),
    (([[1, -1], [-1, 1]], 0), 5),
    (([[904]], 0), 0),
    (([[5]], 5), 1),
    (([[1, 1, 1]], 2), 2),
] + _cases()
