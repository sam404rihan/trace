from helpers import TreeNode


def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> int:
    # Walk down while p and q are on the same side; where they split is the LCA.
    # O(height), O(1) space.
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val
    raise ValueError("p or q is not in the tree")
