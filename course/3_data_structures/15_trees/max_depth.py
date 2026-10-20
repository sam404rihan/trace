r"""
Maximum Depth of Binary Tree                                          [easy] · trees

Return the number of nodes on the longest path from the root down to a leaf.

Example:
        3
       / \
      9  20            max_depth(root)  ->  3
         / \
        15  7

Trees are written as level-order lists with None for a missing child, so the
tree above is [3, 9, 20, None, None, 15, 7]. Nodes have .val, .left and .right.
Try `print_tree(root)` from helpers.py inside your function to see the tree.

Aim for:  O(n) time. Write it recursively, then with a queue (BFS).
Hint:     The depth of a tree is 1 + the depth of its deeper subtree.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def max_depth(root: TreeNode | None) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


USES = ["tree.recursion"]

TESTS = [
    (([3, 9, 20, None, None, 15, 7],), 3),
    (([1, None, 2],), 2),
    (([],), 0),
    (([1],), 1),
    (([1, 2, None, 3, None, 4],), 4),
]
