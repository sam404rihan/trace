"""
What you see from the right                                                  [guided]

Imagine standing to the right of a binary tree. Return the values you can
see, top to bottom: the rightmost node on each level.

Example:
        1
       / \\
      2   3          ->  [1, 3, 4]
       \\
        4

Trees are in level order with None for missing children (see helpers).
"""
from helpers import TreeNode, build_tree


def right_side_view(root: TreeNode | None) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


STEPS = [
    {
        "title": "Full trees",
        "text": "Go level by level (BFS with a queue). The last node you take from each level is the one you see.",
        "hint": "while q: level_size = len(q); for i in range(level_size): node = q.popleft(); ... "
                "if i == level_size - 1: record node.val",
        "tests": [
            (([1, 2, 3, 4, 5, 6, 7],), [1, 3, 7]),
            (([1, 2, 3],), [1, 3]),
        ],
    },
    {
        "title": "Hidden left branches",
        "text": "The rightmost node of a level can be on the LEFT side of the tree, when the right side is shorter.",
        "hint": "Level order handles this for free: you never ask which side a node is on, only whether it's last in its level.",
        "tests": [
            (([1, 2, 3, None, 4],), [1, 3, 4]),
            (([1, 2, 3, 4],), [1, 3, 4]),
            (([1, 2, None, 3, None, 4],), [1, 2, 3, 4]),
        ],
    },
    {
        "title": "Edges",
        "text": "An empty tree shows nothing. A single node shows itself.",
        "hint": "if root is None: return []",
        "tests": [
            (([],), []),
            (([9],), [9]),
            (([1, None, 2, None, 3],), [1, 2, 3]),
        ],
    },
]
