def graph_valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False                    # a tree on n nodes has exactly n - 1 edges
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                # this edge would close a cycle
        parent[ra] = rb
    return True                         # n - 1 edges and no cycle means connected
