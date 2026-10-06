"""
Union-Find (disjoint set union) — tracks which items are in the same group.

    union(1, 2), union(3, 4), union(2, 4)   →   groups: {1, 2, 3, 4}, {5}

Each group is a tree; its root is the group's "representative".
    find(x)       follow parent pointers up to the root
    union(a, b)   point one root at the other

Two tricks make both operations nearly O(1) (technically O(α(n)), where α is the
inverse Ackermann function — under 5 for any n you'll ever see):
    path compression   during find, point every node on the path straight at the root
    union by rank      attach the shorter tree under the taller one

Used for: Kruskal's minimum spanning tree, counting connected components,
detecting cycles in undirected graphs, "accounts merge"-style problems.

Press Run to see the demo at the bottom of this file.
"""


class UnionFind:
    def __init__(self, items=()):
        self.parent = {}
        self.rank = {}
        self.groups = 0
        for x in items:
            self.add(x)

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.groups += 1

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        """Merge the groups of a and b. Returns False if they were already together."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:      # union by rank
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.groups -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


if __name__ == "__main__":
    uf = UnionFind(range(1, 6))
    print("start:", uf.groups, "groups")
    for a, b in [(1, 2), (3, 4), (2, 4)]:
        uf.union(a, b)
        print(f"union({a}, {b}) → {uf.groups} groups")
    print("connected(1, 3):", uf.connected(1, 3))
    print("connected(1, 5):", uf.connected(1, 5))
    print("union(1, 3) again returns", uf.union(1, 3), "— adding edge 1-3 would make a cycle")
