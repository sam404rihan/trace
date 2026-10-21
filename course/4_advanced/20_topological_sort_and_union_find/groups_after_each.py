"""
Groups After Each Friendship                                                  [easy]

n people (0 to n - 1) start as strangers, each in a group of their own. The
friendships in `edges` form one at a time, and friends of friends end up in
the same group. Return the number of groups after each friendship.

Example:
    groups_after_each(4, [[0, 1], [2, 3], [1, 0], [1, 2]])  ->  [3, 2, 2, 1]
        [1, 0] joins two people already in one group, so nothing changes.

Aim for:  about O(n + edges). The last test has 100,000 people and 100,000
          friendships: counting the groups again with BFS after each one times out.
Hint:     Union-find. Keep parent (everyone starts as their own root) and a count of
          groups. For a friendship (a, b), find both roots. If they differ, point
          one root at the other: two groups became one, so subtract 1.
"""


def groups_after_each(n: int, edges: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _fast(n, edges):
    parent, groups, out = list(range(n)), n, []
    for a, b in edges:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        if a != b:
            parent[a] = b
            groups -= 1
        out.append(groups)
    return out


def _big():
    import random
    rng = random.Random(2001)
    edges = [[rng.randrange(100_000), rng.randrange(100_000)] for _ in range(100_000)]
    return (100_000, edges), _fast(100_000, edges)


TEACHES = ["uf.union"]
USES = ["uf.find"]

TESTS = [
    ((4, [[0, 1], [2, 3], [1, 0], [1, 2]]), [3, 2, 2, 1]),
    ((1, []), []),
    ((3, [[0, 0]]), [3]),
    ((5, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 0]]), [4, 3, 3, 2, 1]),
    ((6, [[5, 4], [3, 2], [1, 0], [4, 2], [0, 3]]), [5, 4, 3, 2, 1]),
    _big(),
]
