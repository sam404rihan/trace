"""
Number of Connected Components                                              [medium]

There are n nodes labelled 0 to n - 1 and a list of undirected edges.
Return how many separate groups (connected components) there are.

Example:
    count_components(5, [[0, 1], [1, 2], [3, 4]])  ->  2      {0,1,2} and {3,4}

Aim for:  O(n + edges)
Hint:     Union-find: start with n groups; every union that actually merges
          two groups reduces the count by one. (BFS/DFS from each unvisited
          node works too. Try both.)
"""


def count_components(n: int, edges: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["uf.find", "uf.union"]

TESTS = [
    ((5, [[0, 1], [1, 2], [3, 4]]), 2),
    ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1),
    ((3, []), 3),
    ((4, [[0, 1], [2, 3], [1, 0]]), 2),
    ((1, []), 1),
]
