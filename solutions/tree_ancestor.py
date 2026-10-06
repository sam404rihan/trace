class TreeAncestor:
    def __init__(self, n: int, parent: list[int]):
        self.up = [parent[:]]                       # up[j][v] = the 2^j-th ancestor of v, or -1
        while (1 << len(self.up)) <= n:
            prev = self.up[-1]
            self.up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])

    def get_kth_ancestor(self, node: int, k: int) -> int:
        if k >= 1 << len(self.up):
            return -1
        j = 0
        while k and node != -1:
            if k & 1:
                node = self.up[j][node]
            k >>= 1
            j += 1
        return node
