"""
Insert into a BST                                                           [snippet]

Insert `val` into a binary search tree and return the root. If `val` is
already in the tree, change nothing. An empty tree becomes a single node.

Example:
    tree [4, 2, 7, 1, 3], insert 5   ->   [4, 2, 7, 1, 3, 5]      5 becomes 7's left child

(Trees are shown in level order. The playground builds and reads them for you.)

Hint:     Walk down: smaller goes left, bigger goes right, until the side you
          need is empty. Hang the new node there. Recursive version:
          if root is None: return TreeNode(val); then recurse into one side and reassign it.
"""
from helpers import TreeNode, build_tree, tree_to_list


def bst_insert(root: TreeNode | None, val: int) -> TreeNode:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, val):
    return build_tree(values), val


FINISH = tree_to_list

TESTS = [
    (([4, 2, 7, 1, 3], 5), [4, 2, 7, 1, 3, 5]),
    (([4, 2, 7, 1, 3], 0), [4, 2, 7, 1, 3, None, None, 0]),
    (([], 9), [9]),
    (([4, 2, 7], 2), [4, 2, 7]),
    (([10, 5, 15, None, 7], 6), [10, 5, 15, None, 7, None, None, 6]),
]
