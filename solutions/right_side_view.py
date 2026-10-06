from collections import deque


def right_side_view(root) -> list[int]:
    if root is None:
        return []
    seen, q = [], deque([root])
    while q:
        size = len(q)                     # exactly one level is in the queue right now
        for i in range(size):
            node = q.popleft()
            if i == size - 1:             # last node of this level = visible from the right
                seen.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return seen
