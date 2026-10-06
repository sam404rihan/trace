"""
House Robber III                                                              [medium]

The houses form a binary tree. Robbing two houses that are directly linked
(parent and child) sets off the alarm. Return the most you can take.

Example:
    [3, 2, 3, None, 3, None, 1]   ->  7        3 + 3 + 1
    [3, 4, 5, 1, 3, None, 1]      ->  9        4 + 5

Aim for:  O(n), one postorder pass.
Hint:     Have each node return a pair (rob_it, skip_it). rob_it = node.val + left.skip + right.skip.
          skip_it = max(left) + max(right). The answer is max(pair at the root).
"""
from helpers import TreeNode, build_tree, tree_to_list


def house_robber_iii(root: TreeNode | None) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


def _random_tree_values(rng, n, lo=0, hi=20):
    nodes = [TreeNode(rng.randint(lo, hi)) for _ in range(n)]
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
    nodes, parent, stack = [], {}, [root] if root else []
    while stack:
        n = stack.pop()
        nodes.append(n)
        for c in (n.left, n.right):
            if c:
                parent[c] = n
                stack.append(c)
    best = 0
    for m in range(1 << len(nodes)):
        chosen = {nodes[i] for i in range(len(nodes)) if m >> i & 1}
        if all(parent.get(n) not in chosen for n in chosen):
            best = max(best, sum(n.val for n in chosen))
    return best


def _cases():
    import random
    rng = random.Random(305)
    return [((v,), _brute(v)) for v in (_random_tree_values(rng, rng.randint(0, 12)) for _ in range(8))]


TESTS = [(([3, 2, 3, None, 3, None, 1],), 7), (([3, 4, 5, 1, 3, None, 1],), 9), (([],), 0), (([5],), 5)] + _cases()
