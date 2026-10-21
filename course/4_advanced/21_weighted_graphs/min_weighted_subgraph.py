"""
Minimum Weighted Subgraph With the Required Paths                             [hard]

A directed graph has nodes 0..n-1 and weighted edges [from, to, weight]
(weights > 0). Pick a set of edges so that both src1 and src2 can reach dest
using only the picked edges. Return the smallest possible total weight of the
picked edges, or -1 if it can't be done. (An edge used by both paths is paid once.)

Example:
    min_weighted_subgraph(6, [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3],
                              [2, 3, 4], [3, 4, 2], [4, 5, 1]], 0, 1, 5)  ->  9
    min_weighted_subgraph(3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2)  ->  -1

Aim for:  three runs of Dijkstra: O((n + edges) log n).
Hint:     The best shape is a "Y": both paths walk to some meeting node m, then share one path
          from m to dest. So the answer is min over m of d1[m] + d2[m] + d3[m], where d1 and d2
          are distances from src1 and src2, and d3[m] is the distance from m TO dest: run
          Dijkstra from dest on the graph with every edge reversed.
"""


def min_weighted_subgraph(n: int, edges: list[list[int]], src1: int, src2: int, dest: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _bellman(n, edges, src):
    INF = float("inf")
    d = [INF] * n
    d[src] = 0
    for _ in range(n):
        for a, b, w in edges:
            if d[a] + w < d[b]:
                d[b] = d[a] + w
    return d


def _brute(n, edges, s1, s2, dest):
    """Pairs of shortest-path trees via Bellman-Ford, then the Y formula over every node."""
    d1, d2 = _bellman(n, edges, s1), _bellman(n, edges, s2)
    d3 = _bellman(n, [[b, a, w] for a, b, w in edges], dest)
    best = min(d1[m] + d2[m] + d3[m] for m in range(n))
    return -1 if best == float("inf") else best


def _dijkstra(n, adj, src):
    import heapq
    d = [float("inf")] * n
    d[src] = 0
    h = [(0, src)]
    while h:
        du, u = heapq.heappop(h)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(h, (d[v], v))
    return d


def _fast(n, edges, s1, s2, dest):
    fwd, back = [[] for _ in range(n)], [[] for _ in range(n)]
    for a, b, w in edges:
        fwd[a].append((b, w))
        back[b].append((a, w))
    d1, d2, d3 = _dijkstra(n, fwd, s1), _dijkstra(n, fwd, s2), _dijkstra(n, back, dest)
    best = min(d1[m] + d2[m] + d3[m] for m in range(n))
    return -1 if best == float("inf") else best


def _exhaustive(n, edges, s1, s2, dest):
    """Every subset of edges (only for tiny graphs): checks the Y idea itself."""
    best = None
    for mask in range(1 << len(edges)):
        picked = [e for i, e in enumerate(edges) if mask >> i & 1]
        adj = [[] for _ in range(n)]
        for a, b, _ in picked:
            adj[a].append(b)

        def reaches(s):
            seen, stack = {s}, [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            return dest in seen
        if reaches(s1) and reaches(s2):
            cost = sum(w for _, _, w in picked)
            best = cost if best is None else min(best, cost)
    return -1 if best is None else best


def _cases():
    import random
    rng = random.Random(2203)
    out = []
    for _ in range(6):
        n = rng.randint(3, 5)
        edges = [[*rng.sample(range(n), 2), rng.randint(1, 6)] for _ in range(rng.randint(2, 8))]
        s1, s2, dest = rng.sample(range(n), 3)
        out.append(((n, edges, s1, s2, dest), _exhaustive(n, edges, s1, s2, dest)))
    for _ in range(4):
        n = rng.randint(3, 12)
        edges = [[*rng.sample(range(n), 2), rng.randint(1, 20)] for _ in range(rng.randint(2, 30))]
        s1, s2, dest = rng.sample(range(n), 3)
        out.append(((n, edges, s1, s2, dest), _brute(n, edges, s1, s2, dest)))
    n = 8_000
    edges = [[*rng.sample(range(n), 2), rng.randint(1, 10**5)] for _ in range(25_000)]
    out.append(((n, edges, 0, 1, 2), _fast(n, edges, 0, 1, 2)))
    return out


USES = ["flood.from_targets", "sp.dijkstra"]

TESTS = [
    ((6, [[0, 2, 2], [0, 5, 6], [1, 0, 3], [1, 4, 5], [2, 1, 1], [2, 3, 3], [2, 3, 4], [3, 4, 2], [4, 5, 1]],
      0, 1, 5), 9),
    ((3, [[0, 1, 1], [2, 1, 1]], 0, 1, 2), -1),
    ((3, [[0, 2, 4], [1, 2, 5]], 0, 1, 2), 9),
    ((4, [[0, 2, 1], [1, 2, 1], [2, 3, 10]], 0, 1, 3), 12),
] + _cases()
