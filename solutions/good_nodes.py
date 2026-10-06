def good_nodes(root) -> int:
    count, stack = 0, [(root, float("-inf"))]
    while stack:
        node, best = stack.pop()            # best = biggest value above this node on its path
        if node is None:
            continue
        if node.val >= best:
            count += 1
        best = max(best, node.val)
        stack += [(node.left, best), (node.right, best)]
    return count
