import heapq


def push_keep_k(heap: list[int], x: int, k: int) -> int | None:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)         # the smallest of k+1 is the one that falls out of the top k
    return heap[0] if len(heap) == k else None
