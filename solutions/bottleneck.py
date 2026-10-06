def bottleneck(cap: dict, path: list) -> int:
    return min(cap[u][v] for u, v in pairwise(path))
