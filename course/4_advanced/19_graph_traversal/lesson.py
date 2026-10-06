"""
# Graph traversal (BFS and DFS)

A graph is things (nodes) connected by links (edges). Grids, maps, friend
networks, course prerequisites and word ladders are all graphs.

## Represent it
- **Adjacency list:** `graph = defaultdict(list)`, then `graph[u].append(v)` per edge
  (and `graph[v].append(u)` if undirected). This is what you want 95% of the time
- **Grid:** the cell `(r, c)` is a node; its neighbours are the 4 cells around it:
```
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols: ...
```

## BFS: nearest first (queue)
Use for **shortest path when every step costs the same**, and for "spreading"
(fire, rot, infection) minute by minute.
```
queue, seen = deque([start]), {start}
while queue:
    node = queue.popleft()
    for nxt in graph[node]:
        if nxt not in seen:
            seen.add(nxt)          # mark when you QUEUE it, not when you pop it
            queue.append(nxt)
```
Need distances? Store `(node, dist)` in the queue, or process level by level.
**Multi-source BFS:** start the queue with ALL the sources at once.

## DFS: go deep (recursion or a stack)
Use for "is it connected?", "count the islands/groups", "explore everything".
```
def dfs(node):
    seen.add(node)
    for nxt in graph[node]:
        if nxt not in seen:
            dfs(nxt)
```

## Counting components
Loop over every node; each time you find an unvisited one, that's a new
component. Run BFS/DFS from it to mark the whole group.

## Common mistakes
- Forgetting `seen` on a graph with cycles: infinite loop
- Marking seen when popping (BFS) instead of when pushing: nodes get queued many times
- Using DFS for shortest paths. DFS finds A path, not the shortest
- Recursion depth on big grids (a 300×300 grid can go 90,000 deep). Use an explicit stack

Press Run to see BFS find a shortest path on a grid.
"""
from collections import defaultdict, deque

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)


def bfs_order(start):
    order, seen, queue = [], {start}, deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order


def dfs_order(node, seen=None):
    seen = seen if seen is not None else set()
    seen.add(node)
    order = [node]
    for nxt in graph[node]:
        if nxt not in seen:
            order += dfs_order(nxt, seen)
    return order


print("BFS from A:", bfs_order("A"), "   DFS from A:", dfs_order("A"))

maze = [
    "S.#....",
    ".##.##.",
    "...#...",
    ".#...#E",
]
rows, cols = len(maze), len(maze[0])
start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
parent, queue = {start: None}, deque([start])
while queue:
    r, c = queue.popleft()
    if maze[r][c] == "E":
        break
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in parent:
            parent[(nr, nc)] = (r, c)
            queue.append((nr, nc))

path, cell = set(), (r, c)
while cell:
    path.add(cell)
    cell = parent[cell]
print(f"\nshortest path: {len(path) - 1} steps")
for r in range(rows):
    print("  " + "".join("*" if (r, c) in path and maze[r][c] == "." else maze[r][c] for c in range(cols)))
