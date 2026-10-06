r"""
Graphs — nodes (vertices) connected by edges.

    A ─── B              adjacency list (what we use):
    │     │ \               A: [B, C]
    │     │  E              B: [A, D, E]
    C ─── D                 C: [A, D]      ...

Representations
    adjacency list     dict of node → neighbours.  O(V + E) space. Best for most problems.
    adjacency matrix   V×V grid of 0/1.            O(V²) space. O(1) "is there an edge?"
    grid               a 2D map is a graph: each cell's neighbours are up/down/left/right

Algorithms here                           Time          Use it for
bfs            (queue)                    O(V + E)      shortest path when edges are unweighted
dfs            (stack / recursion)        O(V + E)      reachability, cycles, connected components
shortest_path  (BFS + parent links)       O(V + E)      the actual path, not just its length
topological_sort (Kahn's algorithm)       O(V + E)      ordering tasks with dependencies (DAGs)
dijkstra       (heap)                     O(E log V)    shortest path with non-negative weights

Press Run to see the demo at the bottom of this file.
"""
import heapq
from collections import defaultdict, deque


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = defaultdict(list)        # node -> [(neighbour, weight), ...]

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))
        else:
            self.adj[v]                     # make sure v exists as a node

    def neighbours(self, u):
        return [v for v, _ in self.adj[u]]

    def bfs(self, start):
        """Visit nodes in order of distance from start."""
        order, seen, queue = [], {start}, deque([start])
        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in self.neighbours(node):
                if nxt not in seen:
                    seen.add(nxt)           # mark when queued, not when visited
                    queue.append(nxt)
        return order

    def dfs(self, start):
        """Go as deep as possible before backtracking (recursive version)."""
        order, seen = [], set()

        def visit(node):
            seen.add(node)
            order.append(node)
            for nxt in self.neighbours(node):
                if nxt not in seen:
                    visit(nxt)
        visit(start)
        return order

    def dfs_iterative(self, start):
        order, seen, stack = [], set(), [start]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            order.append(node)
            for nxt in reversed(self.neighbours(node)):   # reversed → same order as recursive
                if nxt not in seen:
                    stack.append(nxt)
        return order

    def shortest_path(self, start, goal):
        """Fewest-edges path using BFS, rebuilt by following parent links back."""
        parent, queue = {start: None}, deque([start])
        while queue:
            node = queue.popleft()
            if node == goal:
                path = []
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return path[::-1]
            for nxt in self.neighbours(node):
                if nxt not in parent:
                    parent[nxt] = node
                    queue.append(nxt)
        return None

    def topological_sort(self):
        """Kahn's algorithm. Returns None if there's a cycle (no valid order)."""
        indegree = {u: 0 for u in self.adj}
        for u in self.adj:
            for v in self.neighbours(u):
                indegree[v] += 1
        ready = deque(u for u in self.adj if indegree[u] == 0)
        order = []
        while ready:
            u = ready.popleft()
            order.append(u)
            for v in self.neighbours(u):
                indegree[v] -= 1
                if indegree[v] == 0:
                    ready.append(v)
        return order if len(order) == len(self.adj) else None

    def dijkstra(self, start):
        """Shortest distance from start to every node (weights must be >= 0)."""
        dist = {start: 0}
        heap = [(0, start)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist.get(u, float("inf")):
                continue                    # stale entry: we already found better
            for v, w in self.adj[u]:
                if d + w < dist.get(v, float("inf")):
                    dist[v] = d + w
                    heapq.heappush(heap, (d + w, v))
        return dist

    def __str__(self):
        return "\n".join(f"  {u}: {self.neighbours(u)}" for u in self.adj)


if __name__ == "__main__":
    g = Graph()
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("B", "E"), ("D", "F")]:
        g.add_edge(u, v)
    print("undirected graph:")
    print(g)
    print("bfs from A:          ", g.bfs("A"))
    print("dfs from A:          ", g.dfs("A"))
    print("dfs (iterative):     ", g.dfs_iterative("A"))
    print("shortest path A → F: ", g.shortest_path("A", "F"))

    tasks = Graph(directed=True)
    for before, after in [("wake up", "shower"), ("wake up", "coffee"), ("shower", "dress"),
                          ("coffee", "leave"), ("dress", "leave")]:
        tasks.add_edge(before, after)
    print("\ntopological order:   ", tasks.topological_sort())

    roads = Graph()
    for u, v, w in [("home", "shop", 4), ("home", "park", 1), ("park", "shop", 2),
                    ("shop", "work", 5), ("park", "work", 8)]:
        roads.add_edge(u, v, w)
    print("dijkstra from home:  ", roads.dijkstra("home"))
