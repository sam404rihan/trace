"""
# Advanced graphs

Beyond BFS and Dijkstra: all-pairs distances, negative edges, two-colourings, and
the structure of a graph (which edges or groups everything depends on).

## Which tool?
- All pairs, n <= ~400: Floyd–Warshall, O(n³)
- Negative edges, or "at most k edges": Bellman–Ford, O(n · E). An improvement in round n means a negative cycle
- "Can it be split into two sides?": bipartite check by BFS colouring
- Critical edges (bridges) / articulation points: Tarjan's low-link, O(n + E)
- Groups that can all reach each other (SCCs): Kosaraju (two DFS passes) or Tarjan
- Edge weights only 0 or 1: 0-1 BFS with a deque (0 → appendleft, 1 → append)

## Floyd–Warshall
```
for k in range(n):            # k OUTERMOST: "paths using only nodes 0..k as stops"
    for i in range(n):
        for j in range(n):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])
```

## Bridges (Tarjan)
```
tin[v] = low[v] = timer++
for each neighbour u (not the edge we came from):
    if visited: low[v] = min(low[v], tin[u])
    else: dfs(u); low[v] = min(low[v], low[u]); if low[u] > tin[v]: (v, u) is a bridge
```

## Common mistakes
- Putting k in an inner loop of Floyd–Warshall
- Deep recursion on big graphs: Python's limit is about 1000, so go iterative or raise the limit
- Treating the parent edge as a back edge in bridge-finding (skip it by edge id, not by node)
"""


INF = float("inf")
d = [[0, 3, INF, 7], [8, 0, 2, INF], [5, INF, 0, 1], [2, INF, INF, 0]]
n = len(d)
for k in range(n):
    for i in range(n):
        for j in range(n):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])
for row in d:
    print(row)
