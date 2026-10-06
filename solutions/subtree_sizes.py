def subtree_sizes(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent, order = [-1] * n, [0]
    seen = [False] * n
    seen[0] = True
    for v in order:                         # BFS: each node appears after its parent
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                parent[w] = v
                order.append(w)
    size = [1] * n
    for v in reversed(order[1:]):           # children before parents
        size[parent[v]] += size[v]
    return size
