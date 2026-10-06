def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(connections):
        adj[a].append((b, i))
        adj[b].append((a, i))
    tin, low = [-1] * n, [0] * n
    timer, bridges = 0, []
    for root in range(n):
        if tin[root] != -1:
            continue
        tin[root] = low[root] = timer
        timer += 1
        stack = [(root, -1, 0)]                 # (node, edge we came in by, next neighbour index)
        while stack:
            v, parent_edge, i = stack[-1]
            if i < len(adj[v]):
                stack[-1] = (v, parent_edge, i + 1)
                u, e = adj[v][i]
                if e == parent_edge:
                    continue                    # don't walk straight back along the same edge
                if tin[u] == -1:
                    tin[u] = low[u] = timer
                    timer += 1
                    stack.append((u, e, 0))
                else:
                    low[v] = min(low[v], tin[u])    # a back edge
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[v])
                    if low[v] > tin[p]:             # v's subtree can't reach above p without this edge
                        bridges.append(sorted((p, v)))
    return sorted(bridges)
