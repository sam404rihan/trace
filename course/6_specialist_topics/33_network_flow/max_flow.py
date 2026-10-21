"""
Maximum Flow                                                                  [guided]

A network has n nodes and directed edges (u, v, capacity). Return the largest total
flow that can go from s to t, where no edge carries more than its capacity and every
other node passes on exactly what it receives. s != t.

Example:
    max_flow(4, [(0, 1, 10), (0, 2, 5), (1, 2, 15), (1, 3, 5), (2, 3, 10)], 0, 3)  ->  15
"""

def _maxflow(n, edges, s, t):
    """Edmonds-Karp on an adjacency dict, for computing expected answers."""
    from collections import deque
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow, cap
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
        flow += push


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _random(seed, count, n, m, cmax):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        edges = []
        for _ in range(m):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                edges.append((u, v, rng.randint(0, cmax)))
        out.append(((n, edges, 0, n - 1), _maxflow(n, edges, 0, n - 1)[0]))
    return out


def _layers(seed, L, W):
    import random
    rng = random.Random(seed)
    n = L * W + 2
    s, t = n - 2, n - 1
    edges = []
    for j in range(W):
        edges.append((s, j, 10**9))
        edges.append(((L - 1) * W + j, t, 10**9))
    for i in range(L - 1):
        for j in range(W):
            for k in rng.sample(range(W), 5):
                edges.append((i * W + j, (i + 1) * W + k, rng.randint(1, 10**6)))
            if rng.random() < 0.5:
                edges.append(((i + 1) * W + rng.randrange(W), i * W + j, rng.randint(1, 10**6)))
    return n, edges, s, t


TEACHES = ["flow.augment"]
USES = ["bfs.shortest", "bfs.path"]

STEPS = [
    {
        "title": "Make it work",
        "text": "Ford-Fulkerson. Keep residual capacities, including a reverse entry for every edge that starts at 0. "
                "Repeatedly find ANY path from s to t using edges with spare capacity (a DFS is fine), push its "
                "bottleneck, subtract it going forward and add it going backward. Stop when no path is left.",
        "hint": "cap = [dict() for _ in range(n)]; for u, v, c: cap[u][v] = cap[u].get(v, 0) + c; cap[v].setdefault(u, 0). "
                "The reverse entries are what let a later path undo an earlier bad choice.",
        "tests": [((4, [(0, 1, 10), (0, 2, 5), (1, 2, 15), (1, 3, 5), (2, 3, 10)], 0, 3), 15),
                  ((4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (1, 2, 1)], 0, 3), 2)] + _random(3302, 6, 8, 20, 20),
    },
    {
        "title": "Edges",
        "text": "No path at all, zero-capacity edges, the same edge listed twice (capacities add up), edges pointing back "
                "into s or out of t, and a case where the greedy first path must be partly undone.",
        "hint": "Parallel edges: add to cap[u][v] rather than overwrite it. If nothing can reach t, the answer is 0.",
        "tests": [((3, [(0, 1, 5)], 0, 2), 0), ((2, [(0, 1, 0)], 0, 1), 0), ((2, [(0, 1, 3), (0, 1, 4)], 0, 1), 7),
                  ((3, [(1, 0, 9), (0, 2, 4), (2, 0, 8), (2, 1, 2)], 0, 2), 4),
                  ((4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 2, 1), (1, 3, 1)], 0, 3), 2)] + _random(3303, 4, 5, 12, 3),
    },
    {
        "title": "Make it fast: BFS paths (Edmonds-Karp)",
        "text": "25 layers of 15 nodes with capacities up to a million. A DFS wanders down long paths whose bottleneck is "
                "tiny, so it needs an enormous number of augmentations. Find each path with BFS instead: the shortest "
                "path in edges. That caps the augmentations at O(V·E) no matter how big the capacities are.",
        "hint": "prev = {s: None}; BFS over edges with cap > 0 until t is reached. Walk prev back from t to collect the "
                "path, take the min capacity, then update cap[u][v] -= push and cap[v][u] += push.",
        "tests": [(_layers(1, 25, 15), 25_938_529), (_layers(2, 25, 15), 24_480_941)],
    },
]
