from helpers import TreeNode


def is_valid_bst(root: TreeNode | None) -> bool:
    # Each node must fit in the open range (low, high) inherited from its
    # ancestors: going left lowers the ceiling, going right raises the floor. O(n).
    def valid(node, low, high):
        if node is None:
            return True
        if not low < node.val < high:
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, float("-inf"), float("inf"))
