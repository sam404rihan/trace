"""
Diameter of a Tree                                                            [medium]

A tree has n nodes (0..n-1) and n - 1 undirected edges. Return the number of edges
on its longest path (the path may start and end anywhere).

Example:
    tree_diameter(6, [(0, 1), (1, 2), (2, 3), (1, 4), (4, 5)])  ->  4      3-2-1-4-5
    tree_diameter(1, [])  ->  0

Aim for:  O(n). The last tests have 100,000 nodes.
Hint:     Two BFS passes. From any node, the farthest node a is always one end of some longest
          path. A BFS from a then reaches the other end, and that distance is the diameter.
"""


def tree_diameter(n: int, edges: list[tuple[int, int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _far(adj, s):
    n = len(adj)
    dist = [-1] * n
    dist[s] = 0
    order = [s]
    for v in order:
        for w in adj[v]:
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                order.append(w)
    end = order[-1]
    return end, dist[end]


def _ref(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    a, _ = _far(adj, 0)
    return _far(adj, a)[1]


def _brute(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return max(_far(adj, s)[1] for s in range(n))


def _cases():
    import random
    rng = random.Random(3207)
    out = []
    for n in (2, 5, 9, 40, 120):
        edges = [(rng.randrange(max(0, v - 3), v), v) for v in range(1, n)]
        out.append(((n, edges), _brute(n, edges)))
    for shape in ("random", "broom"):
        n = 100_000
        if shape == "random":
            edges = [(rng.randrange(v), v) for v in range(1, n)]
        else:
            edges = [(v - 1, v) for v in range(1, 50_000)] + [(rng.randrange(50_000), v) for v in range(50_000, n)]
        out.append(((n, edges), _ref(n, edges)))
    return out


TESTS = [((6, [(0, 1), (1, 2), (2, 3), (1, 4), (4, 5)]), 4), ((1, []), 0), ((2, [(0, 1)]), 1),
         ((5, [(0, 1), (0, 2), (0, 3), (0, 4)]), 2), ((5, [(4, 3), (3, 2), (2, 1), (1, 0)]), 4)] + _cases()
