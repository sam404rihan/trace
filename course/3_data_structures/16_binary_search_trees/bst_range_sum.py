"""
Sum a range in a BST                                                         [guided]

Return the sum of every value in the BST that lies in [lo, hi] (both ends
included).

Example:
    tree [10, 5, 15, 3, 7, None, 18], lo = 7, hi = 15   ->  32      7 + 10 + 15

The BST property lets you skip whole subtrees. That's the point of step 3.
"""
from helpers import TreeNode, build_tree


def bst_range_sum(root: TreeNode | None, lo: int, hi: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, lo, hi):
    return build_tree(values), lo, hi


def _chain(n):
    """1, 2, 3, ..., n inserted in order: a BST that's one long right-leaning chain."""
    out = [1]
    for v in range(2, n + 1):
        out += [None, v]
    return out


_CHAIN = _chain(30_000)

USES = ["bst.walk_down"]

STEPS = [
    {
        "title": "Visit everything",
        "text": "Walk every node (any traversal) and add up the values inside [lo, hi].",
        "hint": "Recursively: (root.val if lo <= root.val <= hi else 0) + sum(left) + sum(right).",
        "tests": [
            (([10, 5, 15, 3, 7, None, 18], 7, 15), 32),
            (([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10), 23),
        ],
    },
    {
        "title": "Edges",
        "text": "An empty tree, a range that misses everything, and a range that's a single value.",
        "hint": "Empty tree: 0.",
        "tests": [
            (([], 1, 5), 0),
            (([4, 2, 6], 10, 20), 0),
            (([4, 2, 6], 6, 6), 6),
        ],
    },
    {
        "title": "Skip what can't match",
        "text": "The last test is a BST that's a 30,000-node chain, and the range is near the top. Visiting everything "
                "recurses 30,000 deep and crashes. Use the BST rule: if root.val < lo, the whole left subtree is too small, "
                "so don't go there. If root.val > hi, skip the right subtree.",
        "hint": "Only recurse left when root.val > lo, and only recurse right when root.val < hi. "
                "(Or use an explicit stack.) Pruning makes it O(height + number of matches).",
        "tests": [
            (([8, 3, 10, 1, 6, None, 14], 4, 9), 14),
            ((_CHAIN, 1, 5), 15),
        ],
    },
]
