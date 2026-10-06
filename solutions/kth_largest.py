import heapq


def kth_largest(nums: list[int], k: int) -> int:
    # Min-heap holding the k largest values so far; its top is the k-th largest.
    # O(n log k) time, O(k) space.
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)    # drop the smallest — it can't be in the top k
    return heap[0]

    # Average O(n): "quickselect" — quicksort's partition, but only recurse
    # into the side that contains position len(nums) - k.
