def path_weight_queries(n: int, edges: list[list[int]], queries: list[list[int]]) -> list[int]:
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    LOG = max(1, n.bit_length())
    up = [[0] * n for _ in range(LOG)]      # up[k][v]: the 2^k-th ancestor of v (root's is root)
    depth = [0] * n
    counts = [None] * n                     # counts[v][w]: weight-w edges from the root to v
    counts[0] = [0] * 27
    visited = [False] * n
    visited[0] = True
    stack = [0]
    while stack:
        u = stack.pop()
        for v, w in graph[u]:
            if not visited[v]:
                visited[v] = True
                up[0][v] = u
                depth[v] = depth[u] + 1
                counts[v] = counts[u][:]
                counts[v][w] += 1
                stack.append(v)
    for k in range(1, LOG):
        for v in range(n):
            up[k][v] = up[k - 1][up[k - 1][v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        lift = depth[a] - depth[b]
        for k in range(LOG):                # bring a up to b's depth
            if lift >> k & 1:
                a = up[k][a]
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):    # climb together while they stay apart
            if up[k][a] != up[k][b]:
                a, b = up[k][a], up[k][b]
        return up[0][a]

    answers = []
    for a, b in queries:
        top = lca(a, b)
        length = depth[a] + depth[b] - 2 * depth[top]
        most = max(counts[a][w] + counts[b][w] - 2 * counts[top][w] for w in range(1, 27))
        answers.append(length - most)       # keep the most common weight, change the rest
    return answers
