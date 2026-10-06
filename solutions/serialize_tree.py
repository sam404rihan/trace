def serialize(root) -> str:
    out = []

    def walk(node):                     # preorder, with "#" for every missing child
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)
    walk(root)
    return ",".join(out)


def deserialize(data: str):
    tokens = iter(data.split(","))

    def build():                        # read the tokens back in the same preorder
        tok = next(tokens)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node
    return build()


def serialize_tree(root):
    data = serialize(root)
    if not isinstance(data, str):
        raise TypeError("serialize must return a str")
    return deserialize(data)
