"""
Many Lowest Common Ancestors                                                  [easy]

A tree has n nodes; parent[v] is v's parent and parent[0] = -1. For each (u, v) in
queries, find their lowest common ancestor: the deepest node that has both u and v in
its subtree (a node counts as its own ancestor). Return the answers in order.

Example:
    parent = [-1, 0, 0, 1, 1, 2, 3]
    lca_queries(parent, [(6, 4), (6, 5), (3, 6), (2, 2)])  ->  [1, 0, 3, 2]

Aim for:  O((n + q) log n). The last test has 60,000 nodes: a very deep chain with long
          branches off its end, and 50,000 queries, most between two different branches.
Hint:     Compute depths (parents can come after children in the list, so use BFS from 0 over
          a children list). Build the lifting table up[j][v]. For a query, lift the deeper node
          by the depth difference. If they're now equal, that's the answer. Otherwise for j from
          high to low, jump both whenever up[j][u] != up[j][v]. Finish with up[0][u].
"""


def lca_queries(parent: list[int], queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


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


def _naive(parent, u, v):
    seen = set()
    while u != -1:
        seen.add(u)
        u = parent[u]
    while v not in seen:
        v = parent[v]
    return v


def _cases():
    import random
    rng = random.Random(3208)
    out = []
    for n in (1, 2, 8, 40, 300):
        perm = list(range(1, n))
        rng.shuffle(perm)
        perm = [0] + perm
        parent = [-1] * n
        for i in range(1, n):
            parent[perm[i]] = perm[rng.randrange(i)]
        qs = [(rng.randrange(n), rng.randrange(n)) for _ in range(30)]
        out.append(((parent, qs), [_naive(parent, u, v) for u, v in qs]))
    parent, depth, lca, tips = _comb(3209, 30_000, 15, 2_000)
    deep = [v for v in range(len(parent)) if depth[v] > 25_000]
    qs = [(rng.choice(tips), rng.choice(tips)) if k % 5 else (rng.choice(deep), rng.choice(deep)) for k in range(50_000)]
    out.append(((parent, qs), [lca(u, v) for u, v in qs]))
    return out


TEACHES = ["tree.lca"]
USES = ["tree.lift_jump", "tree.lift_table", "tree.bfs_order"]

TESTS = [(([-1, 0, 0, 1, 1, 2, 3], [(6, 4), (6, 5), (3, 6), (2, 2)]), [1, 0, 3, 2]), (([-1], [(0, 0)]), [0])] + _cases()
