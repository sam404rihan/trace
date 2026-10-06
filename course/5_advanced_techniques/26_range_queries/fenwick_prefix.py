"""
Fenwick prefix sum                                                          [snippet]

`tree` is a Fenwick tree (binary indexed tree) as a list: tree[0] is unused,
and tree[k] holds the sum of the lowbit(k) = k & -k elements ending at k.
Return the sum of the first i elements.

Example:
    nums [3, 2, -1, 6, 5]  →  tree [0, 3, 5, -1, 10, 5]
    fenwick_prefix(tree, 4)  ->  10        3 + 2 - 1 + 6
    fenwick_prefix(tree, 5)  ->  15        tree[5] + tree[4]

Hint:     s = 0; while i > 0: s += tree[i]; i -= i & -i
          Each step strips the lowest set bit, so it takes at most log2(n) steps.
"""


def fenwick_prefix(tree: list[int], i: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _build(nums):
    tree = [0] * (len(nums) + 1)
    for k, x in enumerate(nums, 1):
        while k < len(tree):
            tree[k] += x
            k += k & -k
    return tree


def _cases():
    import random
    rng = random.Random(201)
    out = []
    for _ in range(8):
        nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 20))]
        i = rng.randint(0, len(nums))
        out.append(((_build(nums), i), sum(nums[:i])))
    return out


TESTS = [((_build([3, 2, -1, 6, 5]), 4), 10), ((_build([3, 2, -1, 6, 5]), 5), 15), ((_build([3, 2, -1, 6, 5]), 0), 0),
         ((_build([7]), 1), 7)] + _cases()
