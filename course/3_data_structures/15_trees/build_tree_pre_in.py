"""
Construct Binary Tree from Preorder and Inorder                               [medium]

Rebuild a binary tree (all values distinct) from its preorder and inorder
traversals, and return the root.

Example:
    preorder [3, 9, 20, 15, 7], inorder [9, 3, 15, 20, 7]   ->   [3, 9, 20, None, None, 15, 7]

Aim for:  O(n).
Hint:     preorder[0] is the root. Find it in inorder: everything to its left is the left subtree,
          and its size tells you how much of preorder belongs to the left. Recurse. A dict
          value → inorder index makes each lookup O(1).
"""
from helpers import TreeNode, build_tree, tree_to_list



def build_tree_pre_in(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    raise NotImplementedError  # replace this line with your solution


FINISH = tree_to_list


def _random_tree_values(rng, n, lo=-20, hi=40, distinct=False):
    """A random binary tree, as a level-order list with None gaps."""
    vals = rng.sample(range(lo, hi), n) if distinct else [rng.randint(lo, hi) for _ in range(n)]
    nodes = [TreeNode(v) for v in vals]
    for i in range(1, n):
        while True:
            parent = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return tree_to_list(nodes[0]) if nodes else []


def _orders(values):
    root, pre, ino = build_tree(values), [], []

    def walk(n):
        if n:
            pre.append(n.val)
            walk(n.left)
            ino.append(n.val)
            walk(n.right)
    walk(root)
    return pre, ino


def _cases():
    import random
    rng = random.Random(66)
    out = []
    for _ in range(10):
        v = _random_tree_values(rng, rng.randint(1, 15), -30, 30, distinct=True)
        pre, ino = _orders(v)
        out.append(((pre, ino), v))
    return out


USES = ["tree.recursion", "tree.inorder"]

TESTS = [(([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, 9, 20, None, None, 15, 7]), (([-1], [-1]), [-1]),
         (([], []), []), (([1, 2, 3], [3, 2, 1]), [1, 2, None, 3])] + _cases()
