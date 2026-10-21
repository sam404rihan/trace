"""
Shortest Paths With Negative Roads                                            [easy]

Places are numbered 0 to n - 1. Each road [a, b, cost] is one-way from a to b,
and a cost can be negative (a road that pays you). No loop of roads has a
negative total. Return the cheapest cost from src to every place, as a list,
with None for places that can't be reached.

Example:
    bellman_ford(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0)  ->  [0, 2, 5]
        Dijkstra settles place 1 at 4 too early: going through place 2 costs 5 - 3 = 2.

Aim for:  O(n * roads).
Hint:     Bellman-Ford. Start with dist[src] = 0 and everything else unknown. Relax every
          road, and repeat that n - 1 times: a cheapest route uses at most n - 1 roads, and
          each round makes at least one more road of it final. Stop early if a round changes
          nothing.
"""


def bellman_ford(n: int, roads: list[list[int]], src: int) -> list[int | None]:
    raise NotImplementedError  # replace this line with your solution


def _fast(n, roads, src):
    dist = [None] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, c in roads:
            if dist[a] is not None and (dist[b] is None or dist[a] + c < dist[b]):
                dist[b] = dist[a] + c
                changed = True
        if not changed:
            break
    return dist


def _big():
    import random
    rng = random.Random(2103)
    n = 300
    roads = [[a, rng.randrange(a + 1, n), rng.randint(-10, 100)] for a in range(n - 1) for _ in range(10)]
    roads += [[rng.randrange(1, n), 0, 5_000] for _ in range(300)]   # back roads cost too much to make a negative loop
    rng.shuffle(roads)
    return (n, roads, 0), _fast(n, roads, 0)


TEACHES = ["sp.bellman_ford"]
USES = ["sp.relax"]

TESTS = [
    ((3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0), [0, 2, 5]),
    ((4, [[0, 1, 1], [0, 2, 3], [2, 1, -5], [1, 3, 1]], 0), [0, -2, 3, -1]),
    ((1, [], 0), [0]),
    ((3, [[1, 2, 7]], 0), [0, None, None]),
    ((4, [[3, 2, -1], [2, 1, -1], [1, 0, -1]], 3), [-3, -2, -1, 0]),
    ((3, [[0, 1, 5], [1, 2, -2], [0, 2, 4], [2, 0, 9]], 0), [0, 5, 3]),
    _big(),
]
