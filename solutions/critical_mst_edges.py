def critical_mst_edges(n: int, edges: list[list[int]]) -> list[list[int]]:
    order = sorted(range(len(edges)), key=lambda i: edges[i][2])

    def mst_weight(skip=-1, force=-1):
        """Kruskal, optionally without one edge or with one edge taken first."""
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total = joined = 0
        if force >= 0:
            a, b, w = edges[force]
            parent[find(a)] = find(b)
            total, joined = w, 1
        for i in order:
            if i == skip:
                continue
            a, b = find(edges[i][0]), find(edges[i][1])
            if a != b:
                parent[a] = b
                total += edges[i][2]
                joined += 1
        return total if joined == n - 1 else inf    # inf: didn't span the graph

    best = mst_weight()
    critical, pseudo = [], []
    for i in range(len(edges)):
        if mst_weight(skip=i) > best:
            critical.append(i)          # every MST needs it
        elif mst_weight(force=i) == best:
            pseudo.append(i)            # some MST uses it, but it can be avoided
    return [critical, pseudo]
