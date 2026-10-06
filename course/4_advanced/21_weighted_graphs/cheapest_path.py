"""
Cheapest path                                                                [guided]

Nodes are 0 to n − 1. Each edge (a, b, w) is a one-way road from a to b
costing w (w ≥ 0). Return the cheapest total cost from src to dst, or -1 if
dst can't be reached.

Example:
    cheapest_path(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)], 0, 3)  ->  4      0 → 2 → 1 → 3
"""


def cheapest_path(n: int, edges: list[tuple[int, int, int]], src: int, dst: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import heapq
    import random
    rng = random.Random(28)
    n = 20_000
    edges = []
    for i in range(1, n):
        edges.append((rng.randrange(i), i, rng.randint(1, 100)))
    for _ in range(100_000):
        edges.append((rng.randrange(n), rng.randrange(n), rng.randint(1, 100)))
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    dist = [float("inf")] * n
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return n, edges, n - 1, dist[n - 1]


_N, _EDGES, _DST, _COST = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Bellman-Ford is the simplest correct method: relax every edge, and repeat n − 1 times. "
                "(After k rounds, every path with at most k edges is accounted for.)",
        "hint": "dist = [inf] * n; dist[src] = 0; repeat n - 1 times: for a, b, w in edges: if dist[a] + w < dist[b]: dist[b] = dist[a] + w",
        "tests": [
            ((4, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)], 0, 3), 4),
            ((3, [(0, 1, 5), (1, 2, 5), (0, 2, 20)], 0, 2), 10),
            ((3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)], 0, 2), 1),
        ],
    },
    {
        "title": "Edges",
        "text": "An unreachable destination returns -1. src == dst costs 0. Roads are one-way. Zero-cost roads are allowed.",
        "hint": "Convert inf to -1 at the end.",
        "tests": [
            ((3, [(0, 1, 2)], 0, 2), -1),
            ((2, [(1, 0, 3)], 0, 1), -1),
            ((5, [(0, 1, 9)], 3, 3), 0),
            ((3, [(0, 1, 0), (1, 2, 0)], 0, 2), 0),
        ],
    },
    {
        "title": "Dijkstra",
        "text": "20,000 nodes and 120,000 roads: n − 1 rounds of relaxing every edge is billions of steps. With no negative "
                "costs, always expand the closest unsettled node next. Its distance can't improve any more. A min-heap "
                "of (distance, node) hands it to you in O(log n).",
        "hint": "Build an adjacency list. pq = [(0, src)]. Pop (d, u); if d > dist[u]: skip (stale). Relax u's edges, "
                "pushing (new_d, v) on improvement. You can stop early when u == dst.",
        "tests": [
            ((5, [(0, 1, 10), (0, 2, 3), (2, 1, 4), (1, 3, 2), (2, 3, 8), (3, 4, 7)], 0, 4), 16),
            ((_N, _EDGES, 0, _DST), _COST),
        ],
    },
]
