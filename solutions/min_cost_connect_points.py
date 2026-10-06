import heapq


def min_cost_connect_points(points: list[list[int]]) -> int:
    # Prim's minimum spanning tree: grow from point 0, always adding the cheapest
    # edge to a point not yet connected. O(n² log n) here, since every pair is an edge.
    n = len(points)
    connected = set()
    heap = [(0, 0)]                      # (cost to connect, point index)
    total = 0
    while len(connected) < n:
        cost, i = heapq.heappop(heap)
        if i in connected:
            continue                     # already joined more cheaply
        connected.add(i)
        total += cost
        xi, yi = points[i]
        for j in range(n):
            if j not in connected:
                xj, yj = points[j]
                heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))
    return total
