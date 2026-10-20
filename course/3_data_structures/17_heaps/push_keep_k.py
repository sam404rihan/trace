"""
Keep the k largest                                                          [snippet]

`heap` is a min-heap (a list kept in heapq order) holding the largest values
seen so far, at most k of them. A new value x arrives. Update the heap so it
still holds the k largest, then return the kth largest so far (the smallest
value in the heap), or None if fewer than k values have been seen.

Example:
    push_keep_k([4, 9, 6], 7, 3)   ->  6      heap becomes [6, 9, 7]; the 3rd largest is 6
    push_keep_k([4, 9, 6], 1, 3)   ->  4      1 is too small to get in
    push_keep_k([5], 8, 3)         ->  None   only 2 values so far

Hint:     heapq.heappush(heap, x); if len(heap) > k: heapq.heappop(heap)
          Popping removes the smallest, which is exactly the one that no longer makes the top k.
"""
import heapq


def push_keep_k(heap: list[int], x: int, k: int) -> int | None:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["heap.top_k"]
USES = []

TESTS = [
    (([4, 9, 6], 7, 3), 6),
    (([4, 9, 6], 1, 3), 4),
    (([5], 8, 3), None),
    (([2, 3], 1, 3), 1),
    (([], 10, 1), 10),
    (([10], 20, 1), 20),
]
