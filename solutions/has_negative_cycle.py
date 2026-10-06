def has_negative_cycle(n: int, edges: list[list[int]]) -> bool:
    dist = [0] * n                      # as if a virtual source reached every node at cost 0
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                changed = True
        if not changed:
            return False                # settled early: no negative cycle
    # One more round: any improvement now can only come from a negative cycle.
    return any(dist[a] + w < dist[b] for a, b, w in edges)
