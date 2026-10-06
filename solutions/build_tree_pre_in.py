def build_tree_pre_in(preorder, inorder):
    where = {v: i for i, v in enumerate(inorder)}
    nxt = iter(preorder)                     # preorder hands out roots in exactly the order we build

    def build(lo, hi):                       # build the subtree whose inorder slice is [lo, hi)
        if lo >= hi:
            return None
        node = TreeNode(next(nxt))
        mid = where[node.val]
        node.left = build(lo, mid)           # left first: preorder lists the left subtree next
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
