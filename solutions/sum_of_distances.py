def sum_of_distances(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent, order, depth = [-1] * n, [0], [0] * n
    seen = [False] * n
    seen[0] = True
    for v in order:                             # BFS order: parents before children
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                parent[w] = v
                depth[w] = depth[v] + 1
                order.append(w)
    size = [1] * n
    for v in reversed(order[1:]):
        size[parent[v]] += size[v]
    ans = [0] * n
    ans[0] = sum(depth)                         # rooted at 0: distances are depths
    for v in order[1:]:                         # reroot from parent to child
        ans[v] = ans[parent[v]] - size[v] + (n - size[v])
    return ans
