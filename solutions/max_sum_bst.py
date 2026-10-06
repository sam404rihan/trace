def max_sum_bst(root: TreeNode | None) -> int:
    best = 0

    def visit(node):
        """(is_bst, smallest, largest, total) for the subtree at node."""
        nonlocal best
        if node is None:
            return True, float("inf"), float("-inf"), 0     # fits under any parent
        l_ok, l_min, l_max, l_sum = visit(node.left)
        r_ok, r_min, r_max, r_sum = visit(node.right)
        if l_ok and r_ok and l_max < node.val < r_min:
            total = l_sum + node.val + r_sum
            best = max(best, total)
            return True, min(l_min, node.val), max(r_max, node.val), total
        return False, 0, 0, 0                               # values don't matter any more

    visit(root)
    return best
