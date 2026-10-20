"""
Inorder Traversal                                                             [easy]

Return the values of a binary tree in in-order: everything in the left
subtree, then the node itself, then everything in the right subtree.

Example:
        1
         \\
          2         ->  [1, 3, 2]
         /
        3

Trees are in level order with None for missing children (see helpers).

Aim for:  O(n). Write it recursively first, then with your own stack.
Hint:     Recursively: inorder(left) + [node.val] + inorder(right). With a stack:
          go left as far as you can, pushing each node; pop one, record it, then
          do the same from its right child.
"""
from helpers import TreeNode, build_tree


def inorder_traversal(root: TreeNode | None) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


TEACHES = ["tree.inorder"]
USES = ["tree.recursion"]

TESTS = [
    (([1, None, 2, 3],), [1, 3, 2]),
    (([],), []),
    (([1],), [1]),
    (([1, 2, 3, 4, 5, None, 6],), [4, 2, 5, 1, 3, 6]),
    (([5, 3, 8, 1, 4, 7, 9],), [1, 3, 4, 5, 7, 8, 9]),
    (([2, 9, 4, None, 7, 1],), [9, 7, 2, 1, 4]),
]
