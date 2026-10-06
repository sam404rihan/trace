"""
Kth Ancestor of a Tree Node                                                   [guided]

A tree has n nodes numbered 0..n-1; parent[i] is the parent of node i, and
parent[0] = -1 (node 0 is the root). Build a class that answers:

    TreeAncestor(n, parent)
    get_kth_ancestor(node, k)     the k-th ancestor of node (k = 1 is the parent), or -1

Example:
    t = TreeAncestor(7, [-1, 0, 0, 1, 1, 2, 2])
    t.get_kth_ancestor(3, 1)  ->  1
    t.get_kth_ancestor(5, 2)  ->  0
    t.get_kth_ancestor(6, 3)  ->  -1
"""


class TreeAncestor:
    def __init__(self, n: int, parent: list[int]):
        raise NotImplementedError

    def get_kth_ancestor(self, node: int, k: int) -> int:
        raise NotImplementedError


CLASS = "TreeAncestor"


def _caterpillar(seed, spine, leaves):
    """A long path 0..spine-1 with leaves hung on random path nodes, relabelled at random (0 stays the root).
    Returns parent (by new label), depth, and lca(u, v) that is O(1) thanks to the construction."""
    import random
    rng = random.Random(seed)
    n = spine + leaves
    hang = [rng.randrange(spine) for _ in range(leaves)]          # leaf i (old label spine + i) hangs on hang[i]
    perm = list(range(1, n))
    rng.shuffle(perm)
    perm = [0] + perm                                               # old label -> new label
    old = [0] * n
    for o, nw in enumerate(perm):
        old[nw] = o
    parent = [-1] * n
    for o in range(1, n):
        parent[perm[o]] = perm[o - 1] if o < spine else perm[hang[o - spine]]

    def depth_old(o):
        return o if o < spine else hang[o - spine] + 1

    def lca(u, v):
        a, b = old[u], old[v]
        if a == b:
            return u
        sa = a if a < spine else hang[a - spine]
        sb = b if b < spine else hang[b - spine]
        if a >= spine and b >= spine:
            return perm[min(sa, sb)]
        if a >= spine:                      # a is a leaf, b on the spine
            return perm[b] if b <= sa else perm[sa]
        if b >= spine:
            return perm[a] if a <= sb else perm[sb]
        return perm[min(a, b)]
    depth = [depth_old(old[v]) for v in range(n)]
    return parent, depth, lca


def _walk(parent, v, k):
    while k and v != -1:
        v, k = parent[v], k - 1
    return v


def _random(seed, count, n, q):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        parent = [-1] + [rng.randrange(v) for v in range(1, n)]
        calls, want = [("TreeAncestor", n, parent)], [None]
        for _ in range(q):
            v, k = rng.randrange(n), rng.randint(1, n)
            calls.append(("get_kth_ancestor", v, k))
            want.append(_walk(parent, v, k))
        out.append((calls, want))
    return out


def _big():
    import random
    rng = random.Random(3203)
    n = 60_000
    parent, depth, _ = _caterpillar(3202, 40_000, 20_000)
    calls, want = [("TreeAncestor", n, parent)], [None]
    deep = [v for v in range(n) if depth[v] > 30_000]
    for _ in range(40_000):
        v = rng.choice(deep)
        k = rng.randint(1, depth[v] + 5)
        calls.append(("get_kth_ancestor", v, k))
        want.append(None)                             # filled in below
    spine_at = {}                                     # every proper ancestor lies on the spine: walk it once
    v = max(range(n), key=lambda x: depth[x])
    while v != -1:
        spine_at[depth[v]] = v
        v = parent[v]
    for i in range(1, len(calls)):
        _, v, k = calls[i]
        d = depth[v] - k
        if d < 0:
            want[i] = -1
        elif k == 0:
            want[i] = v
        else:
            want[i] = spine_at[d]                     # every proper ancestor of any node lies on the spine
    return calls, want


_BIG = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Keep the parent list, and walk up one parent at a time, k times. Stop early at -1.",
        "hint": "while k and node != -1: node = self.parent[node]; k -= 1",
        "tests": [([("TreeAncestor", 7, [-1, 0, 0, 1, 1, 2, 2]), ("get_kth_ancestor", 3, 1), ("get_kth_ancestor", 5, 2),
                    ("get_kth_ancestor", 6, 3)], [None, 1, 0, -1])] + _random(3204, 3, 30, 20),
    },
    {
        "title": "Edges",
        "text": "A single node, asking for the root's parent, k equal to the node's depth exactly (the root), and k far "
                "beyond it.",
        "hint": "Make sure walking off the top returns -1, not an error from parent[-1].",
        "tests": [([("TreeAncestor", 1, [-1]), ("get_kth_ancestor", 0, 1), ("get_kth_ancestor", 0, 50)], [None, -1, -1]),
                  ([("TreeAncestor", 4, [-1, 0, 1, 2]), ("get_kth_ancestor", 3, 3), ("get_kth_ancestor", 3, 4),
                    ("get_kth_ancestor", 3, 10**9)], [None, 0, -1, -1])] + _random(3205, 2, 6, 15),
    },
    {
        "title": "Make it fast: binary lifting",
        "text": "60,000 nodes in a long chain and 40,000 questions with k in the tens of thousands. Walking costs O(k) "
                "each, a billion steps in total. Precompute up[j][v], the 2^j-th ancestor. Then any k is a sum of "
                "powers of two: take one jump per set bit, O(log n) per question.",
        "hint": "up = [parent]; while 2^len(up) <= n: prev = up[-1]; up.append([prev[prev[v]] if prev[v] != -1 else -1 "
                "for v in range(n)]). Query: if k >= 2^len(up) return -1, else for each j with k >> j & 1: node = up[j][node], "
                "stopping at -1.",
        "tests": [_BIG],
    },
]
