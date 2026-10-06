r"""
Binary Tree Level Order Traversal                                   [medium] · trees

Return the node values level by level, left to right.

Example:
        3
       / \
      9  20            level_order(root)  ->  [[3], [9, 20], [15, 7]]
         / \
        15  7

Aim for:  O(n) time
Hint:     Breadth-first search with a queue (collections.deque). At the start of
          each level, len(queue) tells you how many nodes that level has.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def level_order(root: TreeNode | None) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


TESTS = [
    (([3, 9, 20, None, None, 15, 7],), [[3], [9, 20], [15, 7]]),
    (([1],), [[1]]),
    (([],), []),
    (([1, 2, 3, 4, None, None, 5],), [[1], [2, 3], [4, 5]]),
]
