def groups_after_each(n: int, edges: list[list[int]]) -> list[int]:
    # Union-find: a friendship between two different roots merges two groups into one.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving keeps the trees shallow
            x = parent[x]
        return x

    groups, out = n, []
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
        out.append(groups)
    return out
