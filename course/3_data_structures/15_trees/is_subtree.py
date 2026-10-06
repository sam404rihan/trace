"""
Subtree of Another Tree                                                         [easy]

Return True if `sub` appears inside `root`: some node of root whose whole
subtree is identical (same shape, same values) to sub.

Example:
    root [3, 4, 5, 1, 2], sub [4, 1, 2]                          ->  True
    root [3, 4, 5, 1, 2, None, None, None, None, 0], sub [4, 1, 2] ->  False   (4's subtree has an extra 0)

Aim for:  O(m · n) is fine. (Serialising both trees and doing a string search can be faster.)
Hint:     Reuse "same tree": at every node of root, check whether same(node, sub).
"""
from helpers import TreeNode, build_tree, tree_to_list



def is_subtree(root: TreeNode | None, sub: TreeNode | None) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(a, b):
    return build_tree(a), build_tree(b)


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


def _ser(n):
    return "#" if n is None else f"({n.val},{_ser(n.left)},{_ser(n.right)})"


def _brute(a, b):
    sb = _ser(b)
    stack = [a]
    while stack:
        n = stack.pop()
        if _ser(n) == sb:
            return True
        if n:
            stack += [n.left, n.right]
    return False


def _cases():
    import random
    rng = random.Random(64)
    out = []
    for _ in range(10):
        a = _random_tree_values(rng, rng.randint(1, 12), 0, 3)
        b = _random_tree_values(rng, rng.randint(1, 3), 0, 3)
        out.append(((a, b), _brute(build_tree(a), build_tree(b))))
    return out


TESTS = [(([3, 4, 5, 1, 2], [4, 1, 2]), True), (([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]), False),
         (([1, 1], [1]), True), (([12], [2]), False), (([2, 2, None, 2], [2, 2]), True)] + _cases()
