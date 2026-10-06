from collections import deque

from helpers import TreeNode


def max_depth(root: TreeNode | None) -> int:
    # Recursive DFS: depth = 1 + deeper subtree. O(n).
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def max_depth_bfs(root: TreeNode | None) -> int:
    # Iterative BFS: count how many levels we process. O(n).
    if root is None:
        return 0
    depth, queue = 0, deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
