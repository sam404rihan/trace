"""
Minimum Obstacle Removal                                                        [hard]

The grid has 0 (empty) and 1 (obstacle). Moving up, down, left or right into an
empty cell is free, and moving into an obstacle costs 1 (you remove it).
Return the minimum cost from the top-left to the bottom-right corner. Both
corners are empty.

Example:
    min_obstacles([[0, 1, 1], [1, 1, 0], [1, 1, 0]])  ->  2

Aim for:  O(rows · cols) with 0-1 BFS. The last test is 300×300.
Hint:     Dijkstra works, but with only 0/1 weights a deque does it in linear time: pop from the
          left, push 0-cost neighbours to the FRONT and 1-cost neighbours to the BACK. Keep a dist
          grid and only push on improvement.
"""


def min_obstacles(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _dijkstra(g):
    import heapq as hq
    R, C = len(g), len(g[0])
    dist = {(0, 0): 0}
    pq = [(0, 0, 0)]
    while pq:
        d, r, c = hq.heappop(pq)
        if (r, c) == (R - 1, C - 1):
            return d
        if d > dist[(r, c)]:
            continue
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C:
                nd = d + g[x][y]
                if nd < dist.get((x, y), float("inf")):
                    dist[(x, y)] = nd
                    hq.heappush(pq, (nd, x, y))
    return 0


def _cases():
    import random
    rng = random.Random(319)
    out = []
    for size in (2, 3, 4, 5, 6, 8, 300):
        R = C = size
        g = [[1 if rng.random() < 0.45 else 0 for _ in range(C)] for _ in range(R)]
        g[0][0] = g[R - 1][C - 1] = 0
        out.append(((g,), _dijkstra(g)))
    return out


TESTS = [(([[0, 1, 1], [1, 1, 0], [1, 1, 0]],), 2), (([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]],), 0),
         (([[0]],), 0)] + _cases()
