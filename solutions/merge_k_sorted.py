import heapq


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    # The heap holds one "front" item per list: (value, which list, position).
    # Each of the N items is pushed and popped once: O(N log k).
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    merged = []
    while heap:
        value, i, j = heapq.heappop(heap)
        merged.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return merged

    # Standard library: list(heapq.merge(*lists))
