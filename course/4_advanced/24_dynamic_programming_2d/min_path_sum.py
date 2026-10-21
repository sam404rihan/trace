"""
Cheapest path through a grid                                                 [guided]

Each cell of the grid has a cost. Starting top-left and moving only right or
down, reach the bottom-right cell. Return the smallest possible sum of the
cells you pass through (both corners included).

Example:
    min_path_sum([[1, 3, 1],
                  [1, 5, 1],
                  [4, 2, 1]])  ->  7      1 → 3 → 1 → 1 → 1
"""


def min_path_sum(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(32)
    rows, cols = 250, 250
    grid = [[rng.randint(0, 99) for _ in range(cols)] for _ in range(rows)]
    dp = [row[:] for row in grid]
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                continue
            up = dp[r - 1][c] if r else float("inf")
            left = dp[r][c - 1] if c else float("inf")
            dp[r][c] += min(up, left)
    return grid, dp[-1][-1]


_GRID, _BEST = _big()

TEACHES = ["dp.grid"]
USES = []

STEPS = [
    {
        "title": "Recurse from the end",
        "text": "The last step into (r, c) came from above or from the left. So best(r, c) = grid[r][c] + "
                "min(best(r - 1, c), best(r, c - 1)), and best(0, 0) = grid[0][0].",
        "hint": "Treat cells outside the grid as infinitely expensive: return float('inf') when r < 0 or c < 0.",
        "tests": [
            (([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7),
            (([[1, 2, 3], [4, 5, 6]],), 12),
            (([[5, 1], [2, 1]],), 7),
        ],
    },
    {
        "title": "Edges",
        "text": "A single row or column has only one path. A single cell is just its own cost. Zeros are allowed.",
        "hint": "Your base cases should handle these without special code.",
        "tests": [
            (([[1, 2, 3, 4]],), 10),
            (([[1], [2], [3]],), 6),
            (([[42]],), 42),
            (([[0, 0], [0, 0]],), 0),
        ],
    },
    {
        "title": "Fill a table",
        "text": "A 250×250 grid: the plain recursion recomputes the same cells an astronomical number of times. "
                "Fill a table row by row instead. Each cell needs only the cell above it and the cell to its left.",
        "hint": "dp = copy of grid; for each cell (except the corner): dp[r][c] += min(up, left). "
                "Or keep just one row: dp[c] = grid[r][c] + min(dp[c], dp[c - 1]).",
        "tests": [
            (([[1, 9, 9, 9], [1, 1, 9, 9], [9, 1, 1, 1]],), 6),
            ((_GRID,), _BEST),
        ],
    },
]
