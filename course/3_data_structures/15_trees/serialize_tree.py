"""
Serialize and Deserialize a Binary Tree                                         [hard]

Write serialize(root), which turns a tree into a string, and deserialize(data),
which rebuilds exactly the same tree from that string. You choose the format.

The tests call serialize_tree at the bottom, which round-trips the tree through
your two functions. Leave that function as it is.

Example:
    deserialize(serialize(tree [1, 2, 3, None, None, 4, 5]))  ->  the same tree

Aim for:  O(n) both ways.
Hint:     Preorder with a marker for empty children: "1,2,#,#,3,4,#,#,5,#,#". To rebuild, read
          tokens in the same order with an iterator: a "#" means None, otherwise make a node and
          recursively build its left child, then its right child.
"""
from helpers import TreeNode, build_tree, tree_to_list



def serialize(root: TreeNode | None) -> str:
    raise NotImplementedError  # replace this line with your solution


def deserialize(data: str) -> TreeNode | None:
    raise NotImplementedError  # replace this line with your solution


def serialize_tree(root: TreeNode | None) -> TreeNode | None:
    # Don't change this: the tests round-trip the tree through your two functions.
    data = serialize(root)
    if not isinstance(data, str):
        raise TypeError("serialize must return a str")
    return deserialize(data)


def PREPARE(values):
    return (build_tree(values),)


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


def _cases():
    import random
    rng = random.Random(68)
    return [((v,), v) for v in (_random_tree_values(rng, rng.randint(1, 25), -1000, 1000) for _ in range(8))]


USES = ["recursion.parse", "tree.recursion"]

TESTS = [(([1, 2, 3, None, None, 4, 5],), [1, 2, 3, None, None, 4, 5]), (([],), []), (([-7],), [-7]),
         (([1, None, 2, None, 3],), [1, None, 2, None, 3])] + _cases()
