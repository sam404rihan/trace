r"""
Diameter of Binary Tree                                                     [medium]

Return the number of EDGES on the longest path between any two nodes.
The path doesn't have to go through the root.

Example:
          1
         / \
        2   3           ->  3      path 4 -> 2 -> 1 -> 3
       / \
      4   5

Aim for:  O(n), one walk
Hint:     The longest path through a node = height(left) + height(right).
          Write a height() helper that also updates a `best` variable
          (nonlocal) on the way. Return height, record diameter.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def diameter_of_tree(root: TreeNode | None) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


TESTS = [
    (([1, 2, 3, 4, 5],), 3),
    (([1, 2],), 1),
    (([1],), 0),
    (([],), 0),
    (([1, 2, None, 3, 4, 5, None, None, 6],), 4),
]
