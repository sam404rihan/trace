def inorder_traversal(root) -> list[int]:
    # Go left as far as possible, then visit, then turn right. On a BST this is sorted order. O(n).
    out, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out
