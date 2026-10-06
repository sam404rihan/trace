from helpers import TreeNode


def same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    # Compare roots, then both pairs of subtrees. O(n).
    if p is None or q is None:
        return p is q                    # True only if both are None
    return p.val == q.val and same_tree(p.left, q.left) and same_tree(p.right, q.right)
