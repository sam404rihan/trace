"""
Maximal Rectangle                                                             [hard]

`grid` is a list of equal-length strings of "0" and "1". Return the area of the
largest rectangle that contains only "1"s.

Example:
    maximal_rectangle(["10100",
                       "10111",
                       "11111",
                       "10010"])     ->  6       rows 1-2, columns 2-4
    maximal_rectangle(["0"])         ->  0

Aim for:  O(rows * cols).
Hint:     Treat each row as the floor of a histogram: heights[j] = how many "1"s stand in a
          column ending at this row (reset to 0 on a "0"). The answer is the largest rectangle
          in any of those histograms, which a monotonic stack finds in O(cols) (the
          "Largest Rectangle in Histogram" problem).
"""


def maximal_rectangle(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(grid):
    r, c = len(grid), len(grid[0])
    best = 0
    for top in range(r):
        for left in range(c):
            width = c
            for bottom in range(top, r):
                w = 0
                while left + w < c and grid[bottom][left + w] == "1":
                    w += 1
                width = min(width, w)
                if not width:
                    break
                best = max(best, width * (bottom - top + 1))
    return best


def _fast(grid):
    heights, best = [0] * (len(grid[0]) + 1), 0
    for row in grid:
        for j, ch in enumerate(row):
            heights[j] = heights[j] + 1 if ch == "1" else 0
        stack = [-1]
        for j, h in enumerate(heights):
            while stack[-1] != -1 and heights[stack[-1]] >= h:
                top = heights[stack.pop()]
                best = max(best, top * (j - stack[-1] - 1))
            stack.append(j)
    return best


def _cases():
    import random
    rng = random.Random(85)
    out = []
    for _ in range(10):
        cols = rng.randint(1, 7)
        grid = ["".join(rng.choice("0111") for _ in range(cols)) for _ in range(rng.randint(1, 6))]
        out.append(((grid,), _brute(grid)))
    big = ["".join(rng.choice("01111111") for _ in range(150)) for _ in range(150)]
    out.append(((big,), _fast(big)))
    return out


USES = ["stack.monotonic", "stack.span"]

TESTS = [
    ((["10100", "10111", "11111", "10010"],), 6),
    ((["0"],), 0),
    ((["1"],), 1),
    ((["01", "10"],), 1),
    ((["111", "111"],), 6),
] + _cases()
