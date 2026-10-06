"""
Binary Tree Maximum Path Sum                                                    [hard]

A path goes from any node to any node along parent-child links, using each
node at most once (it needn't pass through the root). Return the largest
possible sum of the values on a non-empty path. Values can be negative.

Example:
    [1, 2, 3]                               ->  6        2 → 1 → 3
    [-10, 9, 20, None, None, 15, 7]         ->  42       15 → 20 → 7

Aim for:  O(n): one postorder pass.
Hint:     For each node, compute gain = the best sum of a path that STARTS at this node and goes
          down one side: node.val + max(0, left gain, right gain). The best path that BENDS at
          the node is node.val + max(0, left gain) + max(0, right gain). Track the best bend.
"""
from helpers import TreeNode, build_tree, tree_to_list



def max_path_sum(root: TreeNode) -> int:
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


def _brute(values):
    root = build_tree(values)
    parent, nodes, stack = {}, [], [root]
    while stack:
        n = stack.pop()
        nodes.append(n)
        for c in (n.left, n.right):
            if c:
                parent[c] = n
                stack.append(c)

    def chain(n):
        out = [n]
        while n in parent:
            n = parent[n]
            out.append(n)
        return out
    best = float("-inf")
    for u in nodes:
        cu = chain(u)
        for v in nodes:
            cv = chain(v)
            lca = next(x for x in cu if x in cv)
            path = cu[:cu.index(lca) + 1] + cv[:cv.index(lca)]
            best = max(best, sum(x.val for x in path))
    return best


def _cases():
    import random
    rng = random.Random(67)
    return [((v,), _brute(v)) for v in (_random_tree_values(rng, rng.randint(1, 12), -10, 10) for _ in range(10))]


TESTS = [(([1, 2, 3],), 6), (([-10, 9, 20, None, None, 15, 7],), 42), (([-3],), -3), (([2, -1],), 2),
         (([-2, -1, -3],), -1)] + _cases()
