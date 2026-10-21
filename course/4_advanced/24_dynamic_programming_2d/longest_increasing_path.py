"""
Longest Increasing Path in a Matrix                                             [hard]

From any cell you can move up, down, left or right to a cell with a STRICTLY
larger value. Return the length (in cells) of the longest such path.

Example:
    longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]])  ->  4      1 → 2 → 6 → 9

Aim for:  O(rows · cols): DFS with memoisation.
Hint:     best(r, c) = 1 + max(best of each strictly larger neighbour). There are no cycles,
          because values strictly increase, so caching best(r, c) is safe and makes it linear.
"""


def longest_increasing_path(matrix: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(m):
    R, C = len(m), len(m[0])

    def go(r, c):
        best = 1
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C and m[x][y] > m[r][c]:
                best = max(best, 1 + go(x, y))
        return best
    return max(go(r, c) for r in range(R) for c in range(C))


def _make(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    return ([[rng.randint(0, 9) for _ in range(C)] for _ in range(R)],)


def _snake(n):
    # rises through every cell in a zig-zag: the longest path visits all n * n cells
    return [[r * n + (c if r % 2 == 0 else n - 1 - c) for c in range(n)] for r in range(n)]


def _fast(m):
    R, C = len(m), len(m[0])
    best = [[1] * C for _ in range(R)]
    for v, r, c in sorted(((m[r][c], r, c) for r in range(R) for c in range(C)), reverse=True):
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C and m[x][y] > v:
                best[r][c] = max(best[r][c], 1 + best[x][y])
    return max(max(row) for row in best)


def _big():
    import random
    rng = random.Random(311)
    return [[rng.randint(0, 10**6) for _ in range(180)] for _ in range(180)]


def _cases():
    import random
    rng = random.Random(111)
    out = []
    for _ in range(8):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


_BIG = _big()
USES = ["recursion.memo", "grid.neighbors"]

TESTS = [(([[9, 9, 4], [6, 6, 8], [2, 1, 1]],), 4), (([[3, 4, 5], [3, 2, 6], [2, 2, 1]],), 4), (([[1]],), 1)] + _cases() + \
        [((_snake(30),), 900), ((_BIG,), _fast(_BIG))]
