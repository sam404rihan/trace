"""
Max Area of Island                                                            [medium]

The grid is a list of rows of 0 (water) and 1 (land). An island is land
connected up, down, left or right. Return the area of the largest island, or 0.

Example:
    max_area_island([[1, 1, 0], [0, 1, 0], [0, 0, 1]])  ->  3

Hint:     Like counting islands, but the flood fill returns how many cells it visited.
          Mark cells as you visit them so nothing is counted twice.
"""


def max_area_island(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(g):
    R, C = len(g), len(g[0])
    seen, best = set(), 0
    for r in range(R):
        for c in range(C):
            if g[r][c] and (r, c) not in seen:
                stack, size = [(r, c)], 0
                seen.add((r, c))
                while stack:
                    a, b = stack.pop()
                    size += 1
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < R and 0 <= y < C and g[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                best = max(best, size)
    return best


def _cases():
    import random
    rng = random.Random(84)
    out = []
    for _ in range(8):
        R, C = rng.randint(1, 8), rng.randint(1, 8)
        g = [[1 if rng.random() < 0.5 else 0 for _ in range(C)] for _ in range(R)]
        out.append(((g,), _brute(g)))
    big = [[1 if rng.random() < 0.6 else 0 for _ in range(300)] for _ in range(300)]
    out.append(((big,), _brute(big)))
    return out


USES = ["graph.components", "dfs.flood_fill", "grid.neighbors"]

TESTS = [(([[1, 1, 0], [0, 1, 0], [0, 0, 1]],), 3), (([[0, 0, 0]],), 0), (([[1]],), 1),
         (([[1, 0, 1], [0, 1, 0], [1, 0, 1]],), 1)] + _cases()
