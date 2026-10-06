from collections import deque

from helpers import TreeNode


def level_order(root: TreeNode | None) -> list[list[int]]:
    # BFS; len(queue) at the start of a level is that level's size. O(n).
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
