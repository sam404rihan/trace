"""
Redundant Connection                                                        [medium]

A tree of n nodes (labelled 1 to n) had one extra edge added, creating
exactly one cycle. `edges` lists all n edges. Return the edge that can be
removed to make it a tree again. If several could, return the one that
appears LAST in `edges`.

Example:
    redundant_connection([[1, 2], [1, 3], [2, 3]])  ->  [2, 3]

Aim for:  O(n) with union-find
Hint:     Add the edges one by one with union-find. The first edge whose two
          ends are ALREADY in the same group closes the cycle. That's it.
          (Nodes start at 1, so make parent = list(range(n + 1)).)
"""


def redundant_connection(edges: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def FINISH(result):
    return list(result)  # accept a tuple too


USES = ["uf.find", "uf.union"]

TESTS = [
    (([[1, 2], [1, 3], [2, 3]],), [2, 3]),
    (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4]),
    (([[1, 2], [2, 3], [1, 3]],), [1, 3]),
    (([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]],), [2, 5]),
]
