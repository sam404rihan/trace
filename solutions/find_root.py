def find_root(parent: list[int], x: int) -> int:
    root = x
    while parent[root] != root:         # 1) climb to the root
        root = parent[root]
    while parent[x] != root:            # 2) walk again, pointing everyone straight at it
        parent[x], x = root, parent[x]
    return root
