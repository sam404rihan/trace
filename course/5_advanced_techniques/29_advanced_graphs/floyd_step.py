"""
One Floyd–Warshall round                                                    [snippet]

dist is an n×n matrix of best-known distances (float("inf") = no path yet).
Allow node k as a stopover: for every pair (i, j), if going through k is
shorter, update dist[i][j]. Return dist.

Example:
    dist = [[0, 4, inf], [inf, 0, 1], [2, inf, 0]],  k = 1
    floyd_step(dist, 1)  ->  [[0, 4, 5], [inf, 0, 1], [2, inf, 0]]
    (0 → 2 improves via 1. 2 → 1 doesn't: its route 2 → 0 → 1 needs node 0 as the stop, not node 1.)

Running this for k = 0, 1, …, n-1 IS Floyd–Warshall.

Hint:     for i: for j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
"""


def floyd_step(dist: list[list[float]], k: int) -> list[list[float]]:
    raise NotImplementedError  # replace this line with your solution


INF = float("inf")


def _ref(d, k):
    n = len(d)
    return [[min(d[i][j], d[i][k] + d[k][j]) for j in range(n)] for i in range(n)]


def _cases():
    import random
    rng = random.Random(311)
    out = []
    for _ in range(6):
        n = rng.randint(1, 6)
        d = [[0 if i == j else (rng.randint(1, 9) if rng.random() < 0.5 else INF) for j in range(n)] for i in range(n)]
        k = rng.randrange(n)
        out.append(((d, k), _ref(d, k)))
    return out


TEACHES = ["sp.floyd"]
USES = []

TESTS = [(([[0, 4, INF], [INF, 0, 1], [2, INF, 0]], 1), [[0, 4, 5], [INF, 0, 1], [2, INF, 0]]),
         (([[0]], 0), [[0]])] + _cases()
