"""
Many Lowest Common Ancestors                                                  [easy]

A tree has n nodes; parent[v] is v's parent and parent[0] = -1. For each (u, v) in
queries, find their lowest common ancestor: the deepest node that has both u and v in
its subtree (a node counts as its own ancestor). Return the answers in order.

Example:
    parent = [-1, 0, 0, 1, 1, 2, 3]
    lca_queries(parent, [(6, 4), (6, 5), (3, 6), (2, 2)])  ->  [1, 0, 3, 2]

Aim for:  O((n + q) log n). The last test has 60,000 nodes on a very deep chain and
          50,000 queries.
Hint:     Compute depths (parents can come after children in the list, so use BFS from 0 over
          a children list). Build the lifting table up[j][v]. For a query, lift the deeper node
          by the depth difference. If they're now equal, that's the answer. Otherwise for j from
          high to low, jump both whenever up[j][u] != up[j][v]. Finish with up[0][u].
"""


def lca_queries(parent: list[int], queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


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
    parent, depth, lca = _caterpillar(3209, 35_000, 25_000)
    deep = [v for v in range(len(parent)) if depth[v] > 25_000]
    qs = [(rng.choice(deep), rng.choice(deep)) for _ in range(50_000)]
    out.append(((parent, qs), [lca(u, v) for u, v in qs]))
    return out


TEACHES = ["tree.lca"]
USES = ["tree.lift_jump", "tree.lift_table", "tree.bfs_order"]

TESTS = [(([-1, 0, 0, 1, 1, 2, 3], [(6, 4), (6, 5), (3, 6), (2, 2)]), [1, 0, 3, 2]), (([-1], [(0, 0)]), [0])] + _cases()
