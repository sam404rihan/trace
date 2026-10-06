from helpers import TreeNode


def kth_smallest_bst(root: TreeNode | None, k: int) -> int:
    # Iterative in-order walk (sorted order in a BST); stop at the k-th value.
    # O(h + k): we never visit more than we need.
    stack, node = [], root
    while stack or node:
        while node:                      # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    raise ValueError("k is larger than the tree")
