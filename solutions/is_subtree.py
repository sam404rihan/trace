def is_subtree(root, sub) -> bool:
    def same(a, b):
        if a is None or b is None:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if sub is None:
        return True
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if same(node, sub):
            return True
        stack += [node.left, node.right]
    return False
