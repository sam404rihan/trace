def redundant_connection(edges: list[list[int]]) -> list[int]:
    # Add edges one by one; the first edge joining two already-connected nodes
    # closes the cycle. With exactly one extra edge, that's also the last such edge.
    parent = list(range(len(edges) + 1))     # nodes are 1..n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        parent[ra] = rb
    return []
