r"""
Invert Binary Tree                                                    [easy] · trees

Mirror the tree — swap every node's left and right children — and return
the root.

Example:
        4                  4
       / \                / \
      2   7      ->      7   2
     / \ / \            / \ / \
    1  3 6  9          9  6 3  1

Aim for:  O(n) time
Hint:     Swap the children of the root, then invert each subtree.
"""
from helpers import TreeNode, build_tree, print_tree, tree_to_list  # noqa: F401


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


FINISH = tree_to_list

TESTS = [
    (([4, 2, 7, 1, 3, 6, 9],), [4, 7, 2, 9, 6, 3, 1]),
    (([2, 1, 3],), [2, 3, 1]),
    (([],), []),
    (([1, 2],), [1, None, 2]),
]
