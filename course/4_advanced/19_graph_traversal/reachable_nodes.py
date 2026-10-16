"""
Reachable nodes                                                               [easy]

A graph has nodes 0 to n - 1. `edges` lists undirected edges as pairs (a, b):
you can walk from a to b and from b to a. Return every node you can reach from
`start` (including start itself), sorted.

Example:
    reachable_nodes(5, [(0, 1), (1, 2), (3, 4)], 0)  ->  [0, 1, 2]

Aim for:  O(n + edges).
Hint:     First build the adjacency list: graph = [[] for _ in range(n)], then for each
          edge add b to graph[a] AND a to graph[b]. Then BFS (or DFS) from start with
          a `seen` set, so no node is visited twice.
"""


def reachable_nodes(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["graph.adjacency"]
USES = ["bfs.shortest"]

TESTS = [
    ((5, [(0, 1), (1, 2), (3, 4)], 0), [0, 1, 2]),
    ((5, [(0, 1), (1, 2), (3, 4)], 4), [3, 4]),
    ((3, [], 1), [1]),
    ((4, [(0, 1), (1, 2), (2, 0), (2, 3)], 3), [0, 1, 2, 3]),
    ((6, [(0, 5), (5, 4), (1, 2)], 5), [0, 4, 5]),
]
