"""
# Advanced tree techniques

Plain DFS answers one question about a tree. These techniques answer thousands of
questions quickly by preparing the tree once.

## Use it when
- "k-th ancestor", "lowest common ancestor", "distance between u and v" asked many times
- "For every node, the sum/max of something over the whole tree": rerooting
- Longest path in a tree (the diameter)
- Trees with 10^5 nodes, where recursion depth itself can be a problem

## Binary lifting
up[0][v] = parent of v, and up[j][v] = up[j-1][ up[j-1][v] ]: the 2^j-th ancestor.
To jump k levels, take the jumps for the set bits of k. That's O(log n) per query
after O(n log n) preparation.

LCA(u, v): lift the deeper one to the same depth. If they're equal, done. Otherwise,
for j from high to low, jump both while up[j][u] != up[j][v]. The answer is up[0][u].

## Rerooting
Compute an answer for root 0 with one DFS. Then move the root across each edge and
update in O(1): for sum of distances, moving from p to child c brings size[c] nodes one
step closer and n - size[c] one step farther: ans[c] = ans[p] - size[c] + (n - size[c]).

## Diameter
BFS from any node to the farthest node a. BFS from a, and the farthest distance is the diameter.

## Common mistakes
- Recursion on a 10^5-node path overflows Python's stack: use an explicit stack, or BFS order
- Forgetting that the root's parent is -1 inside the lifting table (jumps must stop there)
- Lifting the wrong node first in LCA (always lift the deeper one)
"""

parent = [-1, 0, 0, 1, 1, 2, 3, 6]          # a small tree: 0 is the root
n, LOG = len(parent), 3
up = [parent[:]]
for j in range(1, LOG + 1):
    prev = up[-1]
    up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])


def kth_ancestor(v, k):
    for j in range(LOG + 1):
        if k >> j & 1:
            v = up[j][v]
            if v == -1:
                break
    return v


depth = [0] * n
for v in range(1, n):                       # parents come before children here
    depth[v] = depth[parent[v]] + 1


def lca(u, v):
    if depth[u] < depth[v]:
        u, v = v, u
    u = kth_ancestor(u, depth[u] - depth[v])
    if u == v:
        return u
    for j in range(LOG, -1, -1):
        if up[j][u] != up[j][v]:
            u, v = up[j][u], up[j][v]
    return up[0][u]


print("up table:", *up, sep="\n  ")
print("3rd ancestor of 7:", kth_ancestor(7, 3))
print("lca(7, 4):", lca(7, 4), "  lca(7, 5):", lca(7, 5))
