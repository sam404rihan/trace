"""
Recover Binary Search Tree                                                    [hard]

Exactly two nodes of this BST had their values swapped by mistake. Fix the tree
IN PLACE by swapping those two values back (don't change its shape). Return
nothing; the test checks the tree afterwards.

Example:
         1                3
        /                /
       3        ->      1
        \\                \\
         2                2

         3                2
        / \\              / \\
       1   4    ->      1   4
          /                /
         2                3

Aim for:  O(n) time. Bonus: O(1) extra space with Morris traversal.
Hint:     The in-order sequence of a BST is increasing. After one swap it has one or two "drops"
          (places where prev.val > node.val). The first wrong node is `prev` at the first drop;
          the second wrong node is `node` at the last drop. Swap their values.
"""
from helpers import TreeNode, build_tree, tree_to_list


def recover_bst(root: TreeNode) -> None:
    raise NotImplementedError  # replace this line with your solution


_ROOT = []


def PREPARE(values):
    _ROOT[:] = [build_tree(values)]
    return (_ROOT[0],)


def FINISH(_):
    return tree_to_list(_ROOT[0])


def _bst(rng, n):
    root = None
    for v in rng.sample(range(0, 80), n):
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
    return root


def _cases():
    import random
    rng = random.Random(99)
    out = []
    for _ in range(10):
        root = _bst(rng, rng.randint(2, 16))
        good = tree_to_list(root)
        nodes, stack = [], [root]
        while stack:
            node = stack.pop()
            nodes.append(node)
            stack += [c for c in (node.left, node.right) if c]
        a, b = rng.sample(nodes, 2)
        a.val, b.val = b.val, a.val
        out.append(((tree_to_list(root),), good))
    return out


TESTS = [
    (([1, 3, None, None, 2],), [3, 1, None, None, 2]),
    (([3, 1, 4, None, None, 2],), [2, 1, 4, None, None, 3]),
    (([3, 1, 2],), [2, 1, 3]),
    (([1, 2],), [2, 1]),
    (([5, 3, 9, 2, 8, 7, 10, None, None, None, None, 6, 4],), [5, 3, 9, 2, 4, 7, 10, None, None, None, None, 6, 8]),
] + _cases()
