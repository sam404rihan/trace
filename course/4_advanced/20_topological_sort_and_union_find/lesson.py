"""
# Topological sort and union-find

Two tools for two classic graph questions:

- **"In what order can I do these tasks?"**: topological sort
- **"Are these two things connected? How many groups are there?"**: union-find

## Topological sort (Kahn's algorithm)
Works on a directed graph of dependencies: edge `a -> b` means a before b.
1. Count each node's incoming edges (its "indegree")
2. Queue every node with indegree 0 (nothing blocks it)
3. Pop a node, add it to the order, and lower the indegree of everything it
   unlocks; queue any that reach 0
4. If the order has fewer nodes than the graph, there's a **cycle**, so no valid order

Spot it: "prerequisites", "build order", "dependencies", "can you finish",
"alien dictionary".

## Union-find (disjoint set union)
Keeps groups. Every item points to a parent; the root is the group's name.
```
parent = list(range(n))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path halving: keeps trees flat
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False                    # already together: this edge makes a cycle
    parent[ra] = rb
    return True
```
Both operations are practically O(1).

Spot it: "number of connected components", "redundant connection",
"accounts merge", "friend circles", edges arriving one at a time.

## BFS/DFS or union-find?
Both count components. Union-find shines when edges arrive one by one, or when
you need to detect the edge that creates a cycle.

Press Run to order some tasks and group some friends.
"""
from collections import deque

tasks = ["wake", "shower", "coffee", "dress", "leave"]
must_come_first = [("wake", "shower"), ("wake", "coffee"), ("shower", "dress"),
                   ("dress", "leave"), ("coffee", "leave")]
unlocks = {t: [] for t in tasks}
indegree = {t: 0 for t in tasks}
for before, after in must_come_first:
    unlocks[before].append(after)
    indegree[after] += 1

ready = deque(t for t in tasks if indegree[t] == 0)
order = []
while ready:
    task = ready.popleft()
    order.append(task)
    for nxt in unlocks[task]:
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            ready.append(nxt)
print("task order:", " -> ".join(order))

people = ["ana", "bo", "cy", "di", "eve"]
index = {name: i for i, name in enumerate(people)}
parent = list(range(len(people)))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    parent[ra] = rb
    return True


for a, b in [("ana", "bo"), ("cy", "di"), ("bo", "ana"), ("di", "eve")]:
    joined = union(index[a], index[b])
    print(f"  friends {a} + {b}: {'merged groups' if joined else 'already in the same group'}")

groups = {}
for name in people:
    groups.setdefault(find(index[name]), []).append(name)
print("groups:", list(groups.values()))
