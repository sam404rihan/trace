"""
Edge-Disjoint Routes                                                            [easy]

A network has n nodes and directed links (u, v); the same link can appear more than
once, meaning several separate cables. How many routes from s to t can run at the
same time if no two routes share a cable? (They may share nodes.)

Example:
    edge_disjoint_paths(4, [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)], 0, 3)  ->  2
    edge_disjoint_paths(3, [(0, 1), (0, 1), (1, 2)], 0, 2)                ->  1

Aim for:  O(answer · E). It's max flow with every capacity equal to 1.
Hint:     Menger's theorem: the number of edge-disjoint paths equals the max flow when each
          cable has capacity 1. Reuse your max_flow, or write the BFS augmenting loop again.
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


def edge_disjoint_paths(n: int, links: list[tuple[int, int]], s: int, t: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(3304)
    out = []
    for n, m in ((4, 8), (6, 15), (10, 40), (40, 200), (300, 3000)):
        links = []
        for _ in range(m):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                links.append((u, v))
        out.append(((n, links, 0, n - 1), _maxflow(n, [(u, v, 1) for u, v in links], 0, n - 1)[0]))
    return out


TESTS = [((4, [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)], 0, 3), 2), ((3, [(0, 1), (0, 1), (1, 2)], 0, 2), 1),
         ((3, [(0, 1), (0, 1), (1, 2), (1, 2), (1, 2)], 0, 2), 2), ((2, [], 0, 1), 0), ((3, [(2, 0), (1, 0)], 0, 2), 0),
         ((6, [(0, 1), (1, 2), (2, 5), (0, 3), (3, 2), (2, 4), (4, 5), (1, 4)], 0, 5), 2)] + _cases()
