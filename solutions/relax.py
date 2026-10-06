def relax(dist: dict, u, v, w: int) -> dict:
    new = dist[u] + w
    if new < dist.get(v, float("inf")):     # strictly better only: ties change nothing
        dist[v] = new
    return dist
