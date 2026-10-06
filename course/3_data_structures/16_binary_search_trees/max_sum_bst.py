"""
Maximum Sum BST in Binary Tree                                                [hard]

Some subtrees of this binary tree may be valid BSTs (every node's left subtree
holds strictly smaller values, its right subtree strictly bigger ones, all the
way down). Return the largest sum of values of any subtree that is a BST.
An empty subtree counts as a BST with sum 0, so the answer is never negative.

Example:
              1
            /   \\
           4     3
          / \\   / \\
         2   4 2   5
                  / \\
                 4   6
    max_sum_bst(...)  ->  20       the subtree rooted at 3: 3 + 2 + 5 + 4 + 6

    max_sum_bst([-4, -2, -5])  ->  0      every subtree sums below 0

Aim for:  O(n), one post-order pass.
Hint:     Have each call return four things about its subtree: is it a BST, its min value, its
          max value, its sum. A node makes a BST when both children do and
          left max < node.val < right min. (Give an empty subtree min = +inf and max = -inf so
          the checks pass.) Update the best sum whenever you find a BST.
"""
from helpers import TreeNode, build_tree, tree_to_list


def max_sum_bst(root: TreeNode | None) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


def _random_tree_values(rng, n):
    """Mostly-BST shapes: insert random keys into a BST, then corrupt a few values."""
    root = None
    for v in rng.sample(range(-20, 40), n):
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
    vals = tree_to_list(root)
    for _ in range(rng.randint(0, 2)):
        i = rng.randrange(len(vals))
        if vals[i] is not None:
            vals[i] = rng.randint(-20, 40)
    return vals


def _brute(values):
    root = build_tree(values)
    best = 0

    def inorder(node, out):
        if node:
            inorder(node.left, out)
            out.append(node.val)
            inorder(node.right, out)
        return out

    stack = [root] if root else []
    while stack:
        node = stack.pop()
        vals = inorder(node, [])
        if all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)):
            best = max(best, sum(vals))
        stack += [c for c in (node.left, node.right) if c]
    return best


def _cases():
    import random
    rng = random.Random(1373)
    return [((vals,), _brute(vals)) for vals in (_random_tree_values(rng, rng.randint(1, 15)) for _ in range(12))]


TESTS = [
    (([1, 4, 3, 2, 4, 2, 5, None, None, None, None, None, None, 4, 6],), 20),
    (([4, 3, None, 1, 2],), 2),
    (([-4, -2, -5],), 0),
    (([2, 1, 3],), 6),
    (([5, 4, 8, 3, None, 6, 3],), 7),
    (([],), 0),
] + _cases()
