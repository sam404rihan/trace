from helpers import TreeNode


def bst_insert(root, val: int):
    if root is None:
        return TreeNode(val)                    # fell off the tree: this is the spot
    if val < root.val:
        root.left = bst_insert(root.left, val)
    elif val > root.val:
        root.right = bst_insert(root.right, val)
    return root                                 # equal: already there, change nothing
