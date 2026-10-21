"""
Cheapest Way to Cut the Network                                               [easy]

A network has n nodes and directed edges (u, v, cost). Choose a set of edges whose
removal leaves no path from s to t, with the smallest possible total cost. Return the
indices (positions in edges) of the edges you remove, in any order. Any cheapest set
is accepted.

Example:
    edges = [(0, 1, 3), (0, 2, 2), (1, 3, 1), (2, 3, 6), (1, 2, 4)]
    min_cut_edges(4, edges, 0, 3)  ->  [0, 1]          cost 3 + 2 = 5 (a cut of [2, 1]: 1 + 6 = 7 costs more)

Aim for:  one max flow, then one search.
Hint:     Max-flow min-cut: after computing the max flow, find every node still reachable from s
          through edges with spare capacity. Call that set S. The cut is every original edge going
          from a node in S to a node outside S; those edges are exactly full. Their costs add up to
          the max flow, so no cheaper cut exists.
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


def min_cut_edges(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected, args):
    """expected is the minimum cost. The chosen edges must cost exactly that and separate s from t."""
    n, edges, s, t = args
    try:
        chosen = set(got)
        if len(chosen) != len(list(got)) or not all(isinstance(i, int) and 0 <= i < len(edges) for i in chosen):
            return False
    except TypeError:
        return False
    if sum(edges[i][2] for i in chosen) != expected:
        return False
    adj = [[] for _ in range(n)]
    for i, (u, v, c) in enumerate(edges):
        if i not in chosen:
            adj[u].append(v)
    seen, stack = {s}, [s]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return t not in seen


def _cases():
    import random
    rng = random.Random(3306)
    out = []
    for n, m, cmax in ((4, 8, 5), (6, 14, 9), (8, 25, 20), (12, 40, 3), (60, 400, 1000), (200, 2500, 10**6)):
        edges = []
        for _ in range(m):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                edges.append((u, v, rng.randint(1, cmax)))
        out.append(((n, edges, 0, n - 1), _maxflow(n, edges, 0, n - 1)[0]))
    return out


TEACHES = ["flow.min_cut"]
USES = ["flow.augment"]

TESTS = [((4, [(0, 1, 3), (0, 2, 2), (1, 3, 1), (2, 3, 6), (1, 2, 4)], 0, 3), 5), ((3, [(0, 1, 4)], 0, 2), 0),
         ((2, [(0, 1, 2), (0, 1, 3)], 0, 1), 5), ((3, [(0, 1, 9), (1, 2, 1), (2, 0, 5)], 0, 2), 1)] + _cases()
