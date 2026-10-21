"""
Min Cost to Connect All Points                                              [medium]

`points` are [x, y] coordinates. Connecting two points costs their Manhattan
distance |x1 - x2| + |y1 - y2|. Return the minimum total cost to connect all
points so there's a path between every pair.

Example:
    min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]])  ->  20

Aim for:  O(n² log n) with Prim's algorithm and a heap (fine for a few hundred points)
Hint:     This is a minimum spanning tree. Start from point 0 with a heap of
          (cost, point). Pop the cheapest; skip it if already connected;
          otherwise add its cost and push edges to every unconnected point.
"""


def min_cost_connect_points(points: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["heap.lazy_delete", "graph.mst"]

TESTS = [
    (([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), 20),
    (([[3, 12], [-2, 5], [-4, 1]],), 18),
    (([[0, 0]],), 0),
    (([[0, 0], [1, 1], [1, 0], [-1, 1]],), 4),
]
