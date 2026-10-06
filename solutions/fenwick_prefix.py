def fenwick_prefix(tree: list[int], i: int) -> int:
    total = 0
    while i > 0:
        total += tree[i]        # tree[i] covers the lowbit(i) elements ending at i
        i -= i & -i             # jump to the block just before them
    return total
