r"""
Validate Binary Search Tree                                         [medium] · trees

Return True if the tree is a valid binary search tree: for every node, ALL
values in its left subtree are smaller and ALL values in its right subtree
are larger (strictly). An empty tree is valid.

Example:
        5
       / \
      1   4          ->  False: 4 is in 5's right subtree but 4 < 5
         / \
        3   6

Aim for:  O(n) time
Hint:     Checking each node against its direct children isn't enough (see the
          third test). Pass down the range (low, high) each node must fit in.
          Alternative: an in-order traversal of a BST is strictly increasing.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def is_valid_bst(root: TreeNode | None) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


USES = ["tree.carry_down"]

TESTS = [
    (([2, 1, 3],), True),
    (([5, 1, 4, None, None, 3, 6],), False),
    (([5, 4, 6, None, None, 3, 7],), False),
    (([1, 1],), False),
    (([],), True),
    (([8, 4, 12, 2, 6, 10, 14],), True),
]
