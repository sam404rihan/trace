def is_balanced(root) -> bool:
    def height(node):
        """Height of the subtree, or -1 if it's unbalanced somewhere inside."""
        if node is None:
            return 0
        left = height(node.left)
        if left < 0:
            return -1
        right = height(node.right)
        if right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return height(root) >= 0
