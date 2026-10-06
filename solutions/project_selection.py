def project_selection(profit: list[int], requires: list[tuple[int, int]]) -> int:
    n = len(profit)
    source, sink = n, n + 1
    cap = [defaultdict(int) for _ in range(n + 2)]      # residual capacities

    def add(u, v, c):
        cap[u][v] += c
        cap[v][u] += 0                                  # make the reverse edge exist

    for i, p in enumerate(profit):
        if p > 0:
            add(source, i, p)           # cut it = give up this profit
        elif p < 0:
            add(i, sink, -p)            # cut it = pay this cost
    for a, b in requires:
        add(a, b, inf)                  # never cut: doing a without b isn't allowed

    def augment():
        """One shortest augmenting path (Edmonds-Karp); returns the flow pushed."""
        prev = {source: None}
        queue = deque([source])
        while queue and sink not in prev:
            u = queue.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    queue.append(v)
        if sink not in prev:
            return 0
        push, v = inf, sink
        while prev[v] is not None:
            push = min(push, cap[prev[v]][v])
            v = prev[v]
        v = sink
        while prev[v] is not None:
            cap[prev[v]][v] -= push
            cap[v][prev[v]] += push
            v = prev[v]
        return push

    min_cut = 0
    while (pushed := augment()):
        min_cut += pushed
    return sum(p for p in profit if p > 0) - min_cut
