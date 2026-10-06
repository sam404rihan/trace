"""
Find with path compression                                                  [snippet]

`parent` is a union-find parent list: parent[x] == x means x is a root.
Return the root of x's group. On the way, point every node you passed
directly at the root ("path compression"), so the next find is instant.

Example:
    parent = [0, 0, 1, 2]          3 → 2 → 1 → 0
    find_root(parent, 3)  ->  0
    parent afterwards: [0, 0, 0, 0]

The tests show (root you returned, parent list afterwards), so both parts are checked.

Hint:     Recursive idea: if parent[x] != x: parent[x] = find_root(parent, parent[x]),
          then return parent[x]. Or two loops: find the root first, then walk again re-pointing.
"""


def find_root(parent: list[int], x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


_SEEN = []


def PREPARE(parent, x):
    _SEEN[:] = [parent]         # remember the list, so we can show it after the call
    return parent, x


def FINISH(root):
    return root, _SEEN[0]


TESTS = [
    (([0, 0, 1, 2], 3), (0, [0, 0, 0, 0])),
    (([0, 1, 2], 2), (2, [0, 1, 2])),
    (([1, 1, 1, 2, 3], 4), (1, [1, 1, 1, 1, 1])),
    (([0, 0, 1, 1, 4, 4], 3), (0, [0, 0, 1, 0, 4, 4])),
]
