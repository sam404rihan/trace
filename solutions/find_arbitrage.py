def find_arbitrage(rates):
    names = sorted({r[0] for r in rates} | {r[1] for r in rates})
    if not names:
        return []
    idx = {c: i for i, c in enumerate(names)}
    edges = [(idx[a], idx[b], -math.log(r)) for a, b, r in rates]   # product > 1  <=>  sum < 0
    n = len(names)
    dist, pred = [0.0] * n, [-1] * n
    last = -1
    for _ in range(n):                          # Bellman–Ford from a virtual source
        last = -1
        for a, b, w in edges:
            if dist[a] + w < dist[b] - 1e-12:
                dist[b] = dist[a] + w
                pred[b] = a
                last = b
        if last == -1:
            return []                           # converged: no negative cycle
    v = last
    for _ in range(n):                          # step back n times to land on the cycle itself
        v = pred[v]
    cycle, u = [v], pred[v]
    while u != v:
        cycle.append(u)
        u = pred[u]
    cycle.append(v)
    cycle.reverse()                             # predecessors run backwards along the trades
    return [names[i] for i in cycle]
