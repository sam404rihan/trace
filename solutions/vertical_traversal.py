def vertical_traversal(root: TreeNode | None) -> list[list[int]]:
    entries = []                            # (col, row, value) for every node
    stack = [(root, 0, 0)] if root else []
    while stack:
        node, row, col = stack.pop()
        entries.append((col, row, node.val))
        if node.left:
            stack.append((node.left, row + 1, col - 1))
        if node.right:
            stack.append((node.right, row + 1, col + 1))
    entries.sort()                          # by column, then row, then value

    columns, last = [], None
    for col, _, val in entries:
        if col != last:
            columns.append([])
            last = col
        columns[-1].append(val)
    return columns
