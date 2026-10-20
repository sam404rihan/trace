import heapq


def k_smallest_sums(a: list[int], b: list[int], k: int) -> list[int]:
    # Each a[i] heads a sorted list a[i] + b[0], a[i] + b[1], ...: a k-way merge. O(k log k).
    heap = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    heapq.heapify(heap)
    out = []
    while len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append(s)
        if j + 1 < len(b):                  # the next sum from the same list
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out
