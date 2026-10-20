r"""
Kth Smallest in a BST                                                       [medium]

Return the k-th smallest value in the binary search tree (k starts at 1).

Example:
        3
       / \
      1   4           k = 1  ->  1
       \
        2

Aim for:  O(h + k), where h is the height: stop as soon as you've seen k values
Hint:     In-order traversal visits a BST in sorted order. Count as you go.
          An iterative in-order walk with a stack lets you stop early.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def kth_smallest_bst(root: TreeNode | None, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, k):
    return (build_tree(values), k)


USES = ["tree.inorder"]

TESTS = [
    (([3, 1, 4, None, 2], 1), 1),
    (([5, 3, 6, 2, 4, None, None, 1], 3), 3),
    (([2, 1, 3], 3), 3),
    (([1], 1), 1),
]
