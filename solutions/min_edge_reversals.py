def min_edge_reversals(n: int, edges: list[list[int]]) -> list[int]:
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append((v, 0))         # along the arrow: free
        graph[v].append((u, 1))         # against it: one reversal
    answer = [0] * n
    parent = [-1] * n
    order, stack = [], [0]
    visited = [False] * n
    visited[0] = True
    while stack:                        # pass 1: cost of reaching everything from node 0
        u = stack.pop()
        order.append(u)
        for v, cost in graph[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                answer[0] += cost
                stack.append(v)
    for u in order:                     # pass 2: parents before children, reroot along each edge
        for v, cost in graph[u]:
            if parent[v] == u:
                # Only the edge u-v changes direction of travel: u→v cost `cost`, v→u costs 1 - cost.
                answer[v] = answer[u] - cost + (1 - cost)
    return answer
