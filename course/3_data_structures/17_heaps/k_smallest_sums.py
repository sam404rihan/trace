"""
Smallest Pair Sums                                                            [easy]

`a` and `b` are sorted. Every pair (a[i], b[j]) has the sum a[i] + b[j].
Return the k smallest of those sums, smallest first. 1 <= k <= len(a) * len(b).

Example:
    k_smallest_sums([1, 7, 11], [2, 4, 6], 3)  ->  [3, 5, 7]      1+2, 1+4 and 1+6

Aim for:  O(k log k). The last test has 100,000 numbers in each list and
          k = 100,000: building every sum means 10 billion pairs.
Hint:     Think of each a[i] as the start of its own sorted list: a[i] + b[0],
          a[i] + b[1], ... Put the first sum of each list (at most k of them) in
          a min-heap as (sum, i, j). Pop the smallest k times, and each time push
          the next sum from the same list, (i, j + 1).
"""


def k_smallest_sums(a: list[int], b: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _fast(a, b, k):
    import heapq
    heap = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    heapq.heapify(heap)
    out = []
    while len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append(s)
        if j + 1 < len(b):
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out


def _big():
    a, b = list(range(0, 200_000, 2)), list(range(0, 300_000, 3))
    return (a, b, 100_000), _fast(a, b, 100_000)


TEACHES = ["heap.k_way_merge"]
USES = []

TESTS = [
    (([1, 7, 11], [2, 4, 6], 3), [3, 5, 7]),
    (([1, 1, 2], [1, 2, 3], 2), [2, 2]),
    (([1, 2], [3], 2), [4, 5]),
    (([5], [5], 1), [10]),
    (([-3, 0, 4], [-1, 2], 6), [-4, -1, -1, 2, 3, 6]),
    (([1, 2, 3], [10, 20, 30], 9), [11, 12, 13, 21, 22, 23, 31, 32, 33]),
    _big(),
]
