def max_staffing(limit: list[int], need: list[int], can: list[tuple[int, int]]) -> int:
    W, P = len(limit), len(need)
    n, s, t = W + P + 2, W + P, W + P + 1
    cap = [dict() for _ in range(n)]

    def edge(u, v, c):
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    for i, c in enumerate(limit):
        edge(s, i, c)                           # worker i takes at most limit[i] projects
    for j, c in enumerate(need):
        edge(W + j, t, c)                       # project j has need[j] seats
    for i, j in can:
        edge(i, W + j, 1)                       # one seat per worker per project
    seats = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return seats
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
        seats += push
