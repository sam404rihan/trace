"""
Cherry Pickup II                                                              [hard]

grid[r][c] is the number of cherries in each cell. Two robots start at the top
row: one in the top-left corner, one in the top-right. Each step, BOTH robots
move down one row, each to column c - 1, c or c + 1 (staying inside the grid).
They pick every cherry on the cells they pass; if both stand on the same cell,
its cherries count once. Return the most cherries they can collect by the
time they reach the bottom row.

Example:
    cherry_pickup_ii([[3, 1, 1],
                      [2, 5, 1],
                      [1, 5, 5],
                      [2, 1, 1]])   ->  24     robot 1: 3, 2, 5, 2;  robot 2: 1, 5, 5, 1

Aim for:  O(rows * cols² * 9).
Hint:     Move the robots together, row by row. The state is (row, c1, c2). From each state,
          try all 3 x 3 moves. dp[c1][c2] = best total with the robots in columns c1 and c2
          on the current row; build the next row's table from it. Count a shared cell once.
"""


def cherry_pickup_ii(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(grid):
    rows, cols = len(grid), len(grid[0])
    best = 0

    def go(r, c1, c2, total):
        nonlocal best
        total += grid[r][c1] + (grid[r][c2] if c2 != c1 else 0)
        if r == rows - 1:
            best = max(best, total)
            return
        for d1 in (-1, 0, 1):
            for d2 in (-1, 0, 1):
                n1, n2 = c1 + d1, c2 + d2
                if 0 <= n1 < cols and 0 <= n2 < cols:
                    go(r + 1, n1, n2, total)
    go(0, 0, cols - 1, 0)
    return best


def _fast(grid):
    rows, cols = len(grid), len(grid[0])
    NEG = float("-inf")
    dp = [[NEG] * cols for _ in range(cols)]
    dp[0][cols - 1] = grid[0][0] + (grid[0][cols - 1] if cols > 1 else 0)
    for r in range(1, rows):
        nxt = [[NEG] * cols for _ in range(cols)]
        for a in range(cols):
            for b in range(cols):
                if dp[a][b] == NEG:
                    continue
                for na in (a - 1, a, a + 1):
                    for nb in (b - 1, b, b + 1):
                        if 0 <= na < cols and 0 <= nb < cols:
                            gain = grid[r][na] + (grid[r][nb] if na != nb else 0)
                            nxt[na][nb] = max(nxt[na][nb], dp[a][b] + gain)
        dp = nxt
    return max(max(row) for row in dp)


def _cases():
    import random
    rng = random.Random(1463)
    out = []
    for _ in range(8):
        g = [[rng.randint(0, 9) for _ in range(rng.randint(1, 5))]]
        g += [[rng.randint(0, 9) for _ in g[0]] for _ in range(rng.randint(0, 4))]
        out.append(((g,), _brute(g)))
    big = [[rng.randint(0, 100) for _ in range(25)] for _ in range(20)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]],), 24),
    (([[1, 0, 0, 0, 0, 0, 1], [2, 0, 0, 0, 0, 3, 0], [2, 0, 9, 0, 0, 0, 0], [0, 3, 0, 5, 4, 0, 0],
       [1, 0, 2, 3, 0, 0, 6]],), 28),
    (([[7]],), 7),
    (([[1, 1], [1, 1]],), 4),
    (([[0, 0, 10, 0, 0], [0, 0, 0, 0, 0]],), 0),
] + _cases()
