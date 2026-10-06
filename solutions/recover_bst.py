def recover_bst(root: TreeNode) -> None:
    first = second = prev = None
    stack, node = [], root
    while stack or node:                # in-order: should be increasing
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev and prev.val > node.val:    # a drop
            if first is None:
                first = prev                # the too-big value is the earlier node of the first drop
            second = node                   # the too-small value is the later node of the last drop
        prev = node
        node = node.right
    first.val, second.val = second.val, first.val
