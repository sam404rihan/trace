"""
# Network flow and matching

Pipes with capacities run from a source s to a sink t. How much can flow through at
once? Max flow answers that, and a surprising number of assignment problems
(matching, scheduling, disjoint paths, cuts) turn into it once you draw the right graph.

## Use it when
- Pair things up as much as possible: workers to jobs, students to projects (bipartite matching)
- "How many edge-disjoint routes", "how many must fail to disconnect"
- Resources with limits on both sides: each worker takes at most 3 shifts, each shift needs 2 people
- Min cut: the cheapest set of edges whose removal separates s from t

## Ford-Fulkerson in one paragraph
Keep a residual graph: for every edge u->v with capacity c and flow f, you can still push
c - f forward, and f backward (undoing flow). Repeatedly find a path from s to t with
spare capacity, push its bottleneck along it, and update both directions. When no path
is left, the flow is maximum.

Edmonds-Karp = find each path with BFS (fewest edges). That bounds the number of
augmentations by O(V·E), whatever the capacities. A plain DFS has no such bound.

## Max-flow min-cut
When the algorithm stops, the nodes still reachable from s in the residual graph form
one side of a minimum cut. The saturated edges leaving that side are the cut, and their
capacities add up to the max flow.

## Modelling tricks
- Bipartite matching: s -> each left node (cap 1), left -> right (cap 1), each right -> t (cap 1)
- A limit on a node: split it into v_in -> v_out with that capacity
- "At most k per person": put k on that person's edge from s

## Common mistakes
- Forgetting the reverse edges, so flow can never be undone
- Overwriting parallel edges (u->v twice) instead of adding the capacities
- Pushing along a path without updating the reverse capacities
"""


def max_flow(n, edges, s, t):
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)                 # the reverse edge starts empty
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:              # BFS for the shortest augmenting path
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
        flow += push
        print("  pushed", push, "along", [s] + [v for _, v in reversed(path)])


edges = [(0, 1, 10), (0, 2, 5), (1, 2, 15), (1, 3, 5), (2, 3, 10)]
print("max flow 0 -> 3:", max_flow(4, edges, 0, 3))
