def bst_range_sum(root, lo: int, hi: int) -> int:
    total, stack = 0, [root]
    while stack:                                # explicit stack: no recursion depth limit
        node = stack.pop()
        if node is None:
            continue
        if lo <= node.val <= hi:
            total += node.val
        if node.val > lo:                       # smaller values might still be in range
            stack.append(node.left)
        if node.val < hi:                       # bigger values might still be in range
            stack.append(node.right)
    return total
