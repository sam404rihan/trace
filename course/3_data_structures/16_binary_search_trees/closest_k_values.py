"""
Closest K Values in a BST                                                     [hard]

Return the k values in the BST that are closest to `target` (a float), sorted
in increasing order. Values are distinct, k <= the number of nodes, and there's
exactly one right answer (no ties in distance).

Example:
            4
          /   \\
         2     5
        / \\
       1   3
    closest_k_values(root, 3.714286, 2)  ->  [3, 4]
    closest_k_values(root, 0.2, 3)       ->  [1, 2, 3]

Aim for:  O(n) by walking the in-order sequence with a window of size k. (With two stacks you
          can even get O(log n + k) on a balanced tree.)
Hint:     In-order traversal visits the values sorted. Keep a deque of at most k values: when it's
          full and the new value is closer than the oldest one, drop the oldest and add the new
          one. Once a new value is NOT closer, every later one is further still: stop.
"""
from helpers import TreeNode, build_tree, tree_to_list


def closest_k_values(root: TreeNode, target: float, k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, target, k):
    return build_tree(values), target, k


def _bst_values(rng, n):
    root = None
    for v in rng.sample(range(0, 60), n):
        if root is None:
            root = TreeNode(v)
            continue
        node = root
        while True:
            side = "left" if v < node.val else "right"
            if getattr(node, side) is None:
                setattr(node, side, TreeNode(v))
                break
            node = getattr(node, side)
    return tree_to_list(root)


def _ref(values, target, k):
    vals = [v for v in values if v is not None]
    return sorted(sorted(vals, key=lambda v: abs(v - target))[:k])


def _cases():
    import random
    rng = random.Random(272)
    out = []
    for _ in range(10):
        vals = _bst_values(rng, rng.randint(1, 15))
        target = rng.randint(-5, 65) + 0.3          # .3 keeps distances from tying
        k = rng.randint(1, sum(v is not None for v in vals))
        out.append(((vals, target, k), _ref(vals, target, k)))
    return out


USES = ["window.fixed", "tree.inorder"]

TESTS = [
    (([4, 2, 5, 1, 3], 3.714286, 2), [3, 4]),
    (([4, 2, 5, 1, 3], 0.2, 3), [1, 2, 3]),
    (([1], 0.0, 1), [1]),
    (([4, 2, 5, 1, 3], 10.0, 5), [1, 2, 3, 4, 5]),
    (([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 6.6, 4), [4, 6, 7, 8]),
] + _cases()
