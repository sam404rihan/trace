"""
Binary Tree Cameras                                                           [hard]

A camera on a node watches that node, its parent and its children. Return the
fewest cameras needed to watch every node of the tree. The tree has at least
one node.

Example:
          0
         /
        0                   ->  1       one camera on the middle node watches all three
       / \\
      0   0

          0
         /
        0
       /
      0                     ->  2
       \\
        0
         \\
          0

Aim for:  O(n), one post-order pass.
Hint:     Decide bottom-up. Each node reports one of three states to its parent: 0 = "not
          watched, I need you to cover me", 1 = "I have a camera", 2 = "watched, no camera".
          A missing child counts as 2. If any child reports 0, put a camera here (return 1).
          Else if any child has a camera, return 2. Else return 0. If the root ends up 0, add
          one more camera for it.
"""
from helpers import TreeNode, build_tree, tree_to_list


def min_cameras(root: TreeNode) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


def _random_tree_values(rng, n):
    nodes = [TreeNode(0) for _ in range(n)]
    for i in range(1, n):
        while True:
            parent = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return tree_to_list(nodes[0])


def _brute(values):
    """Try camera sets in increasing size."""
    from itertools import combinations
    root = build_tree(values)
    nodes, adj, stack = [], {}, [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        adj.setdefault(id(node), {id(node)})
        for child in (node.left, node.right):
            if child:
                adj[id(node)].add(id(child))
                adj.setdefault(id(child), {id(child)}).add(id(node))
                stack.append(child)
    everyone = set(adj)
    for size in range(1, len(nodes) + 1):
        for pick in combinations(nodes, size):
            seen = set()
            for cam in pick:
                seen |= adj[id(cam)]
            if seen == everyone:
                return size


def _cases():
    import random
    rng = random.Random(968)
    return [((vals,), _brute(vals)) for vals in (_random_tree_values(rng, rng.randint(1, 13)) for _ in range(10))]


USES = ["tree.return_and_record"]

TESTS = [
    (([0, 0, None, 0, 0],), 1),
    (([0, 0, None, 0, None, 0, None, None, 0],), 2),
    (([0],), 1),
    (([0, 0],), 1),
    (([0, 0, 0],), 1),
    (([0, 0, 0, 0, 0, 0, 0],), 2),
] + _cases()
