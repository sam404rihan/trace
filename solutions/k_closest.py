import heapq


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    # Size-k MAX-heap of (-distance, x, y): the farthest candidate sits on top,
    # ready to be kicked out. O(n log k).
    heap = []
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))
        if len(heap) > k:
            heapq.heappop(heap)          # drop the farthest
    return [[x, y] for _, x, y in heap]

    # One-liner: heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)
