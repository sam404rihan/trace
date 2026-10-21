def mst_cost(n: int, roads: list[list[int]]) -> int:
    # Kruskal: cheapest roads first; a road that joins two different groups is always worth building.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = built = 0
    for a, b, cost in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra != rb:                        # joins two groups: build it
            parent[ra] = rb
            total += cost
            built += 1
    return total if built == n - 1 else -1  # a tree on n cities has n - 1 roads
