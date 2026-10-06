import heapq


def last_stone(stones: list[int]) -> int:
    heap = [-s for s in stones]     # negate: heapq is a min-heap, we want the heaviest first
    heapq.heapify(heap)             # O(n)
    while len(heap) > 1:
        a = -heapq.heappop(heap)
        b = -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))
    return -heap[0] if heap else 0
