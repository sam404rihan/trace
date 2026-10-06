def max_path_sum(root) -> int:
    best = float("-inf")

    def gain(node):
        """Best sum of a path that starts at node and goes straight down (or is just node)."""
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))      # a negative branch is better left out
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)    # the best path that bends here
        return node.val + max(left, right)

    gain(root)
    return best
