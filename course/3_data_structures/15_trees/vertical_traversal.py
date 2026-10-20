"""
Vertical Order Traversal                                                      [hard]

Put the root at (row 0, column 0). A node at (row, col) has its left child at
(row + 1, col - 1) and its right child at (row + 1, col + 1).

Return the columns from left to right. Within a column, list nodes top to
bottom; nodes in the SAME row and column are listed in increasing value.

Example:
            3
          /   \\
         9     20
              /  \\
             15   7
    vertical_traversal(...)  ->  [[9], [3, 15], [20], [7]]

            1
          /   \\
         2     3
        / \\   / \\
       4   5 6   7
    vertical_traversal(...)  ->  [[4], [2], [1, 5, 6], [3], [7]]     5 and 6 share row 2, column 0

Aim for:  O(n log n).
Hint:     Walk the tree (DFS or BFS) and collect (col, row, value) for every node. Sort those
          tuples: that orders by column, then row, then value. Then group consecutive entries
          with the same column.
"""
from helpers import TreeNode, build_tree, tree_to_list


def vertical_traversal(root: TreeNode | None) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_tree(values),)


def _random_tree_values(rng, n, lo=0, hi=9):
    nodes = [TreeNode(rng.randint(lo, hi)) for _ in range(n)]
    for i in range(1, n):
        while True:
            parent = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(parent, side) is None:
                setattr(parent, side, nodes[i])
                break
    return tree_to_list(nodes[0]) if nodes else []


def _ref(values):
    root = build_tree(values)
    if root is None:
        return []
    cols, frontier, row = {}, [(root, 0)], 0
    while frontier:                                 # level by level, recording rows explicitly
        nxt = []
        for node, col in frontier:
            cols.setdefault(col, {}).setdefault(row, []).append(node.val)
            if node.left:
                nxt.append((node.left, col - 1))
            if node.right:
                nxt.append((node.right, col + 1))
        frontier, row = nxt, row + 1
    return [[v for r in sorted(cols[c]) for v in sorted(cols[c][r])] for c in sorted(cols)]


def _cases():
    import random
    rng = random.Random(987)
    return [((vals,), _ref(vals)) for vals in (_random_tree_values(rng, rng.randint(1, 14)) for _ in range(10))]


USES = ["tree.carry_down"]

TESTS = [
    (([3, 9, 20, None, None, 15, 7],), [[9], [3, 15], [20], [7]]),
    (([1, 2, 3, 4, 5, 6, 7],), [[4], [2], [1, 5, 6], [3], [7]]),
    (([1, 2, 3, 4, 6, 5, 7],), [[4], [2], [1, 5, 6], [3], [7]]),
    (([],), []),
    (([5],), [[5]]),
    (([1, 2, None, 3, None, 4],), [[4], [3], [2], [1]]),
] + _cases()
