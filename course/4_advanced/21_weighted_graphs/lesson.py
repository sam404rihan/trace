"""
# Weighted graphs

When edges have different costs (distance, time, price), plain BFS no longer
finds the cheapest route. Swap its queue for a **heap** and you get Dijkstra.

## Dijkstra: cheapest path from one start to everything
```
dist = {start: 0}
heap = [(0, start)]
while heap:
    d, node = heappop(heap)
    if d > dist[node]:
        continue                         # an outdated entry: skip it
    for nxt, cost in graph[node]:
        if d + cost < dist.get(nxt, inf):
            dist[nxt] = d + cost
            heappush(heap, (d + cost, nxt))
```
- O(E log V)
- The heap always hands you the closest unfinished node, so the first time a
  node is popped (with an up-to-date distance), that distance is final
- **Only works with non-negative weights.** With negative edges, use Bellman-Ford

## Minimum spanning tree (Prim's): connect everything as cheaply as possible
Same heap idea, but the key is the cost of ONE edge, not the total distance:
start anywhere, repeatedly add the cheapest edge that reaches a new node.

Spot it: "connect all", "minimum cost to join", "cables", "roads between all cities".

## Which one?
- Cheapest route from A to B: **Dijkstra**
- Cheapest way to connect all nodes (no single start/end): **MST**
- All edges cost the same: plain **BFS** (simpler and faster)

## Common mistakes
- Forgetting the stale-entry check: correct but much slower
- Pushing `(node, dist)` instead of `(dist, node)`: the heap sorts by the first item
- Using Dijkstra with negative weights

Press Run to find the cheapest routes on a small map.
"""
import heapq
from collections import defaultdict

roads = [("home", "park", 2), ("home", "shop", 7), ("park", "shop", 3),
         ("park", "gym", 8), ("shop", "gym", 2), ("gym", "work", 1), ("shop", "work", 6)]
graph = defaultdict(list)
for a, b, cost in roads:
    graph[a].append((b, cost))
    graph[b].append((a, cost))

dist, came_from = {"home": 0}, {"home": None}
heap = [(0, "home")]
while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]:
        continue
    for nxt, cost in graph[node]:
        if d + cost < dist.get(nxt, float("inf")):
            dist[nxt] = d + cost
            came_from[nxt] = node
            heapq.heappush(heap, (d + cost, nxt))

for place in ["park", "shop", "gym", "work"]:
    path, step = [], place
    while step:
        path.append(step)
        step = came_from[step]
    print(f"home to {place:<5} costs {dist[place]:>2}: {' -> '.join(reversed(path))}")

# Prim's MST on the same map
in_tree, total, heap = {"home"}, 0, [(cost, "home", nxt) for nxt, cost in graph["home"]]
heapq.heapify(heap)
chosen = []
while heap and len(in_tree) < len(graph):
    cost, a, b = heapq.heappop(heap)
    if b in in_tree:
        continue
    in_tree.add(b)
    total += cost
    chosen.append(f"{a}-{b}({cost})")
    for nxt, c in graph[b]:
        if nxt not in in_tree:
            heapq.heappush(heap, (c, b, nxt))
print("\ncheapest way to connect every place:", ", ".join(chosen), "= total", total)
