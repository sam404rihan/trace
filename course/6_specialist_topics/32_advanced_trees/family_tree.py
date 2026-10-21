"""
Family tree                                                                    [build]

A genealogy site stores one family as a tree: parent[v] is v's parent, and parent[0]
is -1 (the founder). Build the lookups behind its "how are we related?" page.

    f = FamilyTree([-1, 0, 0, 1, 1, 2, 3, 3, 6])
    f.common_ancestor(7, 4)   ->  1           the closest shared ancestor
    f.distance(7, 5)          ->  5           steps through the tree: 7-3-1-0-2-5
    f.relation(7, 4)          ->  "cousin 0 removed 1"
    f.relation(3, 4)          ->  "sibling"
    f.relation(1, 8)          ->  "ancestor"

relation(a, b) says what a is to b. Let da and db be how many generations a and b
are below their common ancestor:
  - "self" when a == b
  - "ancestor" when a is above b on the same line (da == 0), "descendant" when db == 0
  - "sibling" when da == db == 1
  - otherwise "cousin D removed R" with D = min(da, db) - 1 and R = |da - db|
    (so an aunt or uncle is "cousin 0 removed 1", and first cousins are "cousin 1 removed 0")

Aim for:  O(log n) per question. The last test has 60,000 people in a very deep line
          with long branches, and 50,000 questions.
Hint:     This is binary lifting plus depths. common_ancestor is LCA. distance is
          depth[a] + depth[b] - 2·depth[lca]. relation reads da and db off the depths.
"""


class FamilyTree:
    def __init__(self, parent: list[int]):
        raise NotImplementedError

    def common_ancestor(self, a: int, b: int) -> int:
        raise NotImplementedError

    def distance(self, a: int, b: int) -> int:
        raise NotImplementedError

    def relation(self, a: int, b: int) -> str:
        raise NotImplementedError


CLASS = "FamilyTree"


def _comb(seed, spine, arms, arm_len):
    """A long path 0..spine-1 with `arms` paths of arm_len nodes hung on random nodes near its far end,
    relabelled at random (0 stays the root). Two nodes deep on different arms meet far above both.
    Returns parent (by new label), depth, lca(u, v) that is O(1) thanks to the construction, and tips:
    the nodes on the far half of their arm."""
    import random
    rng = random.Random(seed)
    n = spine + arms * arm_len
    hang = [rng.randrange(spine - 10_000, spine) for _ in range(arms)]  # arm k hangs on path node hang[k]
    perm = list(range(1, n))
    rng.shuffle(perm)
    perm = [0] + perm                                               # old label -> new label
    old = [0] * n
    for o, nw in enumerate(perm):
        old[nw] = o
    parent = [-1] * n
    for o in range(1, n):
        if o < spine:
            parent[perm[o]] = perm[o - 1]
        else:
            k, i = divmod(o - spine, arm_len)
            parent[perm[o]] = perm[hang[k]] if i == 0 else perm[o - 1]

    def place(o):
        """(arm, step along the arm, path node it hangs on); arm is -1 for a path node."""
        if o < spine:
            return -1, 0, o
        k, i = divmod(o - spine, arm_len)
        return k, i, hang[k]

    def lca(u, v):
        (ka, ia, ha), (kb, ib, hb) = place(old[u]), place(old[v])
        if ka == kb:
            return u if (ia <= ib if ka >= 0 else ha <= hb) else v
        if ka >= 0 and kb >= 0:
            return perm[min(ha, hb)]
        if ka >= 0:                         # u on an arm, v on the path
            return v if hb <= ha else perm[ha]
        return u if ha <= hb else perm[hb]
    depth = [0] * n
    for v in range(n):
        k, i, h = place(old[v])
        depth[v] = h if k < 0 else h + 1 + i
    tips = [v for v in range(n) if place(old[v])[1] >= arm_len // 2]
    return parent, depth, lca, tips


def _answer(op, a, b, depth, lca):
    c = lca(a, b)
    if op == "common_ancestor":
        return c
    if op == "distance":
        return depth[a] + depth[b] - 2 * depth[c]
    da, db = depth[a] - depth[c], depth[b] - depth[c]
    if a == b:
        return "self"
    if da == 0:
        return "ancestor"
    if db == 0:
        return "descendant"
    if da == db == 1:
        return "sibling"
    return f"cousin {min(da, db) - 1} removed {abs(da - db)}"


def _small(seed, n, q):
    import random
    rng = random.Random(seed)
    perm = list(range(1, n))
    rng.shuffle(perm)
    perm = [0] + perm
    parent = [-1] * n
    for i in range(1, n):
        parent[perm[i]] = perm[rng.randrange(max(0, i - 3), i)]
    depth = [0] * n
    for v in range(n):
        d, w = 0, v
        while parent[w] != -1:
            w, d = parent[w], d + 1
        depth[v] = d

    def lca(a, b):
        seen = set()
        while a != -1:
            seen.add(a)
            a = parent[a]
        while b not in seen:
            b = parent[b]
        return b
    calls, want = [("FamilyTree", parent)], [None]
    for _ in range(q):
        op = rng.choice(["common_ancestor", "distance", "relation", "relation"])
        a, b = rng.randrange(n), rng.randrange(n)
        calls.append((op, a, b))
        want.append(_answer(op, a, b, depth, lca))
    return calls, want


def _big():
    import random
    rng = random.Random(3212)
    parent, depth, lca, tips = _comb(3211, 30_000, 15, 2_000)
    n = len(parent)
    deep = [v for v in range(n) if depth[v] > 25_000]
    calls, want = [("FamilyTree", parent)], [None]
    for k in range(50_000):
        op = rng.choice(["common_ancestor", "distance", "relation"])
        a, b = (rng.choice(tips), rng.choice(tips)) if k % 5 else (rng.choice(deep), rng.choice(deep))
        calls.append((op, a, b))
        want.append(_answer(op, a, b, depth, lca))
    return calls, want


USES = ["tree.lift_jump", "tree.lift_table", "tree.bfs_order", "tree.lca"]

TESTS = [([("FamilyTree", [-1, 0, 0, 1, 1, 2, 3, 3, 6]), ("common_ancestor", 7, 4), ("distance", 7, 5), ("relation", 7, 4),
           ("relation", 3, 4), ("relation", 1, 8), ("relation", 8, 1), ("relation", 6, 7), ("relation", 8, 5), ("relation", 2, 2)],
          [None, 1, 5, "cousin 0 removed 1", "sibling", "ancestor", "descendant", "sibling", "cousin 1 removed 2", "self"]),
         ([("FamilyTree", [-1]), ("relation", 0, 0), ("distance", 0, 0), ("common_ancestor", 0, 0)], [None, "self", 0, 0])] \
    + [_small(3213 + k, n, 60) for k, n in enumerate((2, 5, 12, 30, 80))] + [_big()]
