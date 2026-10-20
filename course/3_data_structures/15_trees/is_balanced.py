"""
Balanced Binary Tree                                                            [easy]

A tree is height-balanced if, at EVERY node, the heights of the left and right
subtrees differ by at most 1. Return True if the tree is balanced.

Example:
    [3, 9, 20, None, None, 15, 7]          ->  True
    [1, 2, 2, 3, 3, None, None, 4, 4]      ->  False

Aim for:  O(n): one bottom-up pass, not a height computation at every node.
Hint:     Have a helper return the height, or -1 meaning "already unbalanced below".
          Once a child returns -1, pass -1 straight up.
"""
from helpers import TreeNode, build_tree, tree_to_list



def is_balanced(root: TreeNode | None) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


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


def _brute(root):
    def h(n):
        return 0 if n is None else 1 + max(h(n.left), h(n.right))

    def ok(n):
        return n is None or (abs(h(n.left) - h(n.right)) <= 1 and ok(n.left) and ok(n.right))
    return ok(root)


def _cases():
    import random
    rng = random.Random(63)
    out = []
    for _ in range(10):
        v = _random_tree_values(rng, rng.randint(0, 12))
        out.append(((v,), _brute(build_tree(v))))
    return out


USES = ["tree.recursion"]

TESTS = [(([3, 9, 20, None, None, 15, 7],), True), (([1, 2, 2, 3, 3, None, None, 4, 4],), False), (([],), True),
         (([1, None, 2, None, 3],), False), (([1, 2, 3, 4, None, None, 5],), True)] + _cases()
