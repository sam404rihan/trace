"""
Count Good Nodes in a Binary Tree                                             [medium]

A node is "good" if no node on the path from the root down to it has a bigger
value. Return how many good nodes the tree has. (The root is always good.)

Example:
    [3, 1, 4, 3, None, 1, 5]  ->  4        3, 4, 5, and the lower 3

Aim for:  O(n): one walk down the tree.
Hint:     DFS, carrying the maximum value seen so far on the path. A node is good if its value
          is >= that maximum. Pass the new maximum down to its children.
"""
from helpers import TreeNode, build_tree, tree_to_list



def good_nodes(root: TreeNode | None) -> int:
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
    count, stack = 0, [(root, [])]
    while stack:
        n, path = stack.pop()
        if n is None:
            continue
        if all(p <= n.val for p in path):
            count += 1
        stack += [(n.left, path + [n.val]), (n.right, path + [n.val])]
    return count


def _cases():
    import random
    rng = random.Random(65)
    return [((v,), _brute(build_tree(v))) for v in (_random_tree_values(rng, rng.randint(1, 15), -5, 10) for _ in range(10))]


USES = ["tree.carry_down"]

TESTS = [(([3, 1, 4, 3, None, 1, 5],), 4), (([3, 3, None, 4, 2],), 3), (([1],), 1), (([],), 0)] + _cases()
