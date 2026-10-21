"""
Swim in Rising Water                                                            [hard]

grid is n×n and holds every number 0 .. n²-1 once: the height of each cell.
At time t the water is at level t everywhere, and you can swim between
adjacent cells (up, down, left, right) only if both are at height <= t.
Return the least time at which you can get from the top-left corner to the
bottom-right corner.

Example:
    swim_rising_water([[0, 2], [1, 3]])  ->  3

Aim for:  O(n² log n). It's a shortest path where the "cost" of a route is its highest cell.
Hint:     Dijkstra with a min-heap keyed by the highest height seen on the route so far:
          max(current, neighbour height). The first time you pop the corner, that's the answer.
          (Binary search on t plus BFS also works.)
"""


def swim_rising_water(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(grid):
    n = len(grid)

    def ok(t):
        if grid[0][0] > t:
            return False
        seen, stack = {(0, 0)}, [(0, 0)]
        while stack:
            r, c = stack.pop()
            if (r, c) == (n - 1, n - 1):
                return True
            for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= x < n and 0 <= y < n and (x, y) not in seen and grid[x][y] <= t:
                    seen.add((x, y))
                    stack.append((x, y))
        return False
    return next(t for t in range(n * n) if ok(t))


def _cases():
    import random
    rng = random.Random(92)
    out = []
    for n in (1, 2, 3, 4, 5, 6, 7):
        vals = list(range(n * n))
        rng.shuffle(vals)
        g = [vals[r * n:(r + 1) * n] for r in range(n)]
        out.append(((g,), _brute(g)))
    return out


USES = ["grid.neighbors", "sp.dijkstra"]

TESTS = [(([[0, 2], [1, 3]],), 3),
         (([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]],), 16)] + _cases()
