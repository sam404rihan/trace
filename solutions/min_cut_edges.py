def min_cut_edges(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> list[int]:
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    while True:                                 # Edmonds-Karp until no augmenting path is left
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            break
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
    side = set(prev)                            # the last BFS reached exactly the source side
    return [i for i, (u, v, _) in enumerate(edges) if u in side and v not in side]
