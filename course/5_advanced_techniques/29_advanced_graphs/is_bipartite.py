"""
Is Graph Bipartite?                                                           [medium]

graph[i] lists the neighbours of node i (undirected). Can the nodes be coloured
with two colours so that every edge joins different colours? The graph may be
in several pieces.

Example:
    is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]])        ->  True      a 4-cycle
    is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]])  ->  False     a triangle 0-1-2

Aim for:  O(n + E).
Hint:     BFS from every uncoloured node. Give it colour 0, and each neighbour the opposite colour.
          A neighbour that already has the SAME colour as you is a contradiction (an odd cycle).
"""


def is_bipartite(graph: list[list[int]]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(graph):
    n = len(graph)
    edges = [(a, b) for a in range(n) for b in graph[a] if a < b]
    return any(all((m >> a & 1) != (m >> b & 1) for a, b in edges) for m in range(1 << n))


def _cases():
    import random
    rng = random.Random(315)
    out = []
    for _ in range(10):
        n = rng.randint(1, 9)
        adj = [set() for _ in range(n)]
        for _ in range(rng.randint(0, n + 2)):
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                adj[a].add(b)
                adj[b].add(a)
        g = [sorted(s) for s in adj]
        out.append(((g,), _brute(g)))
    return out


TESTS = [(([[1, 3], [0, 2], [1, 3], [0, 2]],), True), (([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],), False), (([[]],), True),
         (([[1], [0], [3], [2]],), True)] + _cases()
