from helpers import TreeNode


def diameter_of_tree(root: TreeNode | None) -> int:
    # height() returns what the parent needs (height) and records what we
    # want (the longest path through each node) on the side. O(n).
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)   # edges on the path through this node
        return 1 + max(left, right)

    height(root)
    return best
