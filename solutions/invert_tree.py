from helpers import TreeNode


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    # Swap children, then recurse into both. O(n).
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
