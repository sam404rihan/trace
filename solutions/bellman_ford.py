def bellman_ford(n: int, roads: list[list[int]], src: int) -> list[int | None]:
    # Relax every road, n - 1 rounds at most. Negative roads are fine as long as no loop is negative.
    dist = [None] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, cost in roads:
            if dist[a] is not None and (dist[b] is None or dist[a] + cost < dist[b]):
                dist[b] = dist[a] + cost
                changed = True
        if not changed:                     # nothing improved: every distance is final
            break
    return dist
