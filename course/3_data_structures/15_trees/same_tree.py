"""
Same Tree                                                                     [easy]

Return True if the two trees have exactly the same shape and values.

Example:
    [1, 2, 3] and [1, 2, 3]       ->  True
    [1, 2]    and [1, None, 2]    ->  False    (2 is a left child vs a right child)

Aim for:  O(n)
Hint:     Both empty: True. Exactly one empty: False. Otherwise the values
          match AND both left subtrees are the same AND both right ones are.
"""
from helpers import TreeNode, build_tree, print_tree  # noqa: F401


def same_tree(p: TreeNode | None, q: TreeNode | None) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(a, b):
    return (build_tree(a), build_tree(b))


USES = ["tree.recursion"]

TESTS = [
    (([1, 2, 3], [1, 2, 3]), True),
    (([1, 2], [1, None, 2]), False),
    (([1, 2, 1], [1, 1, 2]), False),
    (([], []), True),
    (([1], []), False),
]
