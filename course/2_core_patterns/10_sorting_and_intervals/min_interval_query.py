"""
Minimum Interval to Include Each Query                                          [hard]

Each interval [l, r] has size r - l + 1. For every query q, return the size of
the SMALLEST interval with l <= q <= r, or -1 if none contains it. Answers go
in the same order as the queries.

Example:
    min_interval_query([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5])  ->  [3, 3, 1, 4]

Aim for:  O((n + q) log n): offline, with sorting and a heap. The last test is big.
Hint:     Sort intervals by start, and handle queries in increasing order (remembering where each
          answer goes). For a query, push every interval starting <= q into a min-heap of
          (size, end). Pop while the top's end < q. The top, if any, is the answer.
"""


def min_interval_query(intervals: list[list[int]], queries: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(iv, qs):
    return [min((r - l + 1 for l, r in iv if l <= q <= r), default=-1) for q in qs]


def _make(rng):
    iv = []
    for _ in range(rng.randint(1, 8)):
        l = rng.randint(1, 15)
        iv.append([l, l + rng.randint(0, 6)])
    return (iv, [rng.randint(0, 22) for _ in range(rng.randint(1, 8))])


def _fast(iv, qs):
    import heapq as hq
    iv = sorted(iv)
    out, heap, i = {}, [], 0
    for q in sorted(set(qs)):
        while i < len(iv) and iv[i][0] <= q:
            hq.heappush(heap, (iv[i][1] - iv[i][0] + 1, iv[i][1]))
            i += 1
        while heap and heap[0][1] < q:
            hq.heappop(heap)
        out[q] = heap[0][0] if heap else -1
    return [out[q] for q in qs]


def _big():
    import random
    rng = random.Random(222)
    iv = []
    for _ in range(60_000):
        l = rng.randint(1, 10**7)
        iv.append([l, l + rng.randint(0, 10**5)])
    qs = [rng.randint(1, 10**7) for _ in range(60_000)]
    return iv, qs


def _cases():
    import random
    rng = random.Random(122)
    out = []
    for _ in range(12):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


_BIV, _BQS = _big()
TESTS = [(([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]), [3, 3, 1, 4]),
         (([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]), [2, -1, 4, 6])] + _cases() + \
        [((_BIV, _BQS), _fast(_BIV, _BQS))]
