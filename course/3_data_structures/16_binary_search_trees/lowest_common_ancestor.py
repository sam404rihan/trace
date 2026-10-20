r"""
Lowest Common Ancestor of a BST                                             [medium]

Return the VALUE of the lowest node that has both p and q in its subtree
(a node counts as being in its own subtree). p and q are values in the tree.

Example:
            6
          /   \
         2     8          p = 2, q = 8  ->  6
        / \   / \         p = 2, q = 4  ->  2
       0   4 7   9
          / \
         3   5

Aim for:  O(height), without visiting the whole tree
Hint:     Use the BST rule. If both are smaller than the node, go left; both
          bigger, go right. Otherwise they split here, so this is the answer.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, p, q):
    return (build_tree(values), p, q)


USES = ["bst.walk_down"]

TESTS = [
    (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8), 6),
    (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4), 2),
    (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5), 4),
    (([2, 1], 2, 1), 2),
]
