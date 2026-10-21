"""
Relax an edge                                                               [snippet]

`dist` maps each node to the best distance found so far (missing means "not
reached yet", i.e. infinity). There's an edge u → v with weight w, and
dist[u] is known. If going through u is shorter, update dist[v]. Return dist.

Example:
    relax({"A": 0, "B": 5}, "A", "B", 3)   ->  {"A": 0, "B": 3}
    relax({"A": 0, "B": 2}, "A", "B", 3)   ->  {"A": 0, "B": 2}     no improvement
    relax({"A": 4}, "A", "C", 1)           ->  {"A": 4, "C": 5}     first time reaching C

Every shortest-path algorithm (Dijkstra, Bellman-Ford) is this step, repeated
in a clever order.

Hint:     new = dist[u] + w;  if new < dist.get(v, float("inf")): dist[v] = new
"""


def relax(dist: dict, u, v, w: int) -> dict:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["sp.relax"]
USES = []

TESTS = [
    (({"A": 0, "B": 5}, "A", "B", 3), {"A": 0, "B": 3}),
    (({"A": 0, "B": 2}, "A", "B", 3), {"A": 0, "B": 2}),
    (({"A": 4}, "A", "C", 1), {"A": 4, "C": 5}),
    (({"A": 1, "B": 3}, "A", "B", 2), {"A": 1, "B": 3}),
]
