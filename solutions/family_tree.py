class FamilyTree:
    def __init__(self, parent: list[int]):
        n = len(parent)
        children = [[] for _ in range(n)]
        for v in range(1, n):
            children[parent[v]].append(v)
        self.depth, order = [0] * n, [0]
        for v in order:
            for c in children[v]:
                self.depth[c] = self.depth[v] + 1
                order.append(c)
        self.up = [parent[:]]                       # up[j][v] = the 2^j-th ancestor of v
        while (1 << len(self.up)) <= n:
            prev = self.up[-1]
            self.up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])

    def common_ancestor(self, a: int, b: int) -> int:
        depth, up = self.depth, self.up
        if depth[a] < depth[b]:
            a, b = b, a
        diff, j = depth[a] - depth[b], 0
        while diff:
            if diff & 1:
                a = up[j][a]
            diff >>= 1
            j += 1
        if a == b:
            return a
        for j in range(len(up) - 1, -1, -1):
            if up[j][a] != up[j][b]:
                a, b = up[j][a], up[j][b]
        return up[0][a]

    def distance(self, a: int, b: int) -> int:
        c = self.common_ancestor(a, b)
        return self.depth[a] + self.depth[b] - 2 * self.depth[c]

    def relation(self, a: int, b: int) -> str:
        if a == b:
            return "self"
        c = self.common_ancestor(a, b)
        da, db = self.depth[a] - self.depth[c], self.depth[b] - self.depth[c]
        if da == 0:
            return "ancestor"
        if db == 0:
            return "descendant"
        if da == db == 1:
            return "sibling"
        return f"cousin {min(da, db) - 1} removed {abs(da - db)}"
