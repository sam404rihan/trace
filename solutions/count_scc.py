def count_scc(n: int, edges: list[list[int]]) -> int:
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        radj[b].append(a)
    seen, order = [False] * n, []
    for s in range(n):                          # pass 1: record finishing order (iterative DFS)
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, 0)]
        while stack:
            v, i = stack[-1]
            if i < len(adj[v]):
                stack[-1] = (v, i + 1)
                u = adj[v][i]
                if not seen[u]:
                    seen[u] = True
                    stack.append((u, 0))
            else:
                order.append(v)
                stack.pop()
    seen, count = [False] * n, 0
    for s in reversed(order):                   # pass 2: on the reversed graph, latest finisher first
        if seen[s]:
            continue
        count += 1                              # everything reached now is one component
        seen[s] = True
        stack = [s]
        while stack:
            for u in radj[stack.pop()]:
                if not seen[u]:
                    seen[u] = True
                    stack.append(u)
    return count
