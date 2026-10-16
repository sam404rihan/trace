"""
Clone Graph                                                                   [medium]

Each Node has .val (1..n, all different) and .neighbors (a list of Nodes).
Given one node of a connected undirected graph, return a deep copy of the whole
graph: all brand-new nodes, with the same edges.

Tests write the graph as an adjacency list: adj[i] lists the neighbour values of
node i + 1. Your copy is read back the same way, and must not reuse any
original node.

Example:
    [[2, 4], [1, 3], [2, 4], [1, 3]]   (a square 1-2-3-4-1)  copies to the same shape

Hint:     DFS or BFS with a dict original → copy. Create a node's copy the first time you see it.
          Then for each neighbour, append that neighbour's copy (creating it if needed).
"""


class Node:
    def __init__(self, val: int = 0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Node | None) -> Node | None:
    raise NotImplementedError  # replace this line with your solution


_ORIGINAL = []


def PREPARE(adj):
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[v - 1] for v in nbrs]
    _ORIGINAL[:] = [set(map(id, nodes))]
    return (nodes[0] if nodes else None,)


def FINISH(start):
    if start is None:
        return []
    seen, order = {id(start): start}, [start]
    i = 0
    while i < len(order):
        for nb in order[i].neighbors:
            if id(nb) not in seen:
                seen[id(nb)] = nb
                order.append(nb)
        i += 1
    if any(id(n) in _ORIGINAL[0] for n in order):
        return "reused an original node instead of copying it"
    by_val = sorted(order, key=lambda n: n.val)
    return [[nb.val for nb in n.neighbors] for n in by_val]


def _cases():
    import random
    rng = random.Random(85)
    out = []
    for _ in range(5):
        n = rng.randint(2, 9)
        edges = {(i, rng.randrange(i)) for i in range(1, n)}
        for _ in range(rng.randint(0, n)):
            a, b = rng.sample(range(n), 2)
            edges.add((max(a, b), min(a, b)))
        adj = [[] for _ in range(n)]
        for a, b in sorted(edges):
            adj[a].append(b + 1)
            adj[b].append(a + 1)
        out.append(((adj,), adj))
    return out


USES = ["graph.adjacency"]

TESTS = [(([[2, 4], [1, 3], [2, 4], [1, 3]],), [[2, 4], [1, 3], [2, 4], [1, 3]]), (([[]],), [[]]), (([],), []),
         (([[2], [1]],), [[2], [1]])] + _cases()
