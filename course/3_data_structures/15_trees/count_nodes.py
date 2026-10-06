"""
Count the nodes                                                             [snippet]

Return how many nodes a binary tree has.

Trees in the tests are written in level order, with None for a missing child:
[1, 2, 3, None, 4] is 1 with children 2 and 3, where 2 has a right child 4.
The playground builds the TreeNode objects for you (.val, .left, .right).

Example:
    count_nodes(tree [1, 2, 3, None, 4])  ->  4

Hint:     The tree-recursion template: an empty tree has 0 nodes. Otherwise it's
          1 (this node) + the count on the left + the count on the right.
"""
from helpers import TreeNode, build_tree


def count_nodes(root: TreeNode | None) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


TESTS = [
    (([1, 2, 3, None, 4],), 4),
    (([],), 0),
    (([7],), 1),
    (([1, 2, 3, 4, 5, 6, 7],), 7),
    (([1, None, 2, None, 3],), 3),
]
