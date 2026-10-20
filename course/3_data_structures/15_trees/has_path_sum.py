r"""
Path Sum                                                                      [easy]

Return True if some path from the root down to a LEAF adds up to `target`.
A leaf is a node with no children.

Example:
          5
         / \
        4   8
       /   / \
      11  13  4           target 22  ->  True     5 + 4 + 11 + 2
     /  \      \
    7    2      1

Aim for:  O(n)
Hint:     Pass the remaining amount down: has_path_sum(child, target - node.val).
          Check for the target only when you're AT a leaf.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def has_path_sum(root: TreeNode | None, target: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, target):
    return (build_tree(values), target)


TEACHES = ["tree.carry_down"]
USES = ["tree.recursion"]

TESTS = [
    (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22), True),
    (([1, 2, 3], 5), False),
    (([], 0), False),
    (([1, 2], 1), False),
    (([1, 2], 3), True),
]
