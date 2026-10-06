def lca_queries(parent: list[int], queries: list[tuple[int, int]]) -> list[int]:
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    depth, order = [0] * n, [0]
    for v in order:                                 # BFS from the root for depths
        for c in children[v]:
            depth[c] = depth[v] + 1
            order.append(c)
    up = [parent[:]]
    while (1 << len(up)) <= n:
        prev = up[-1]
        up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff, j = depth[u] - depth[v], 0
        while diff:                                 # lift the deeper node to the same depth
            if diff & 1:
                u = up[j][u]
            diff >>= 1
            j += 1
        if u == v:
            return u
        for j in range(len(up) - 1, -1, -1):        # jump both while they stay below the answer
            if up[j][u] != up[j][v]:
                u, v = up[j][u], up[j][v]
        return up[0][u]

    return [lca(u, v) for u, v in queries]
