"""
Find Median from Data Stream                                                  [easy]

Numbers arrive one at a time. Build a class:

    add_num(x)      add a number
    find_median()   the median of everything so far, as a float
                    (the average of the two middle values when the count is even)

Example:
    m = MedianFinder()
    m.add_num(1); m.add_num(2)
    m.find_median()   ->  1.5
    m.add_num(3)
    m.find_median()   ->  2.0

Aim for:  O(log n) add, O(1) median.
Hint:     Two heaps: a max-heap `low` for the smaller half (heappush_max / heappop_max, or negatives) and a min-heap `high`
          for the larger half. Keep every value in low <= every value in high, and len(low) equal
          to len(high) or one more. Then the median is the top of low, or the average of both tops.
"""


class MedianFinder:
    def __init__(self):
        raise NotImplementedError

    def add_num(self, x: int) -> None:
        raise NotImplementedError

    def find_median(self) -> float:
        raise NotImplementedError


CLASS = "MedianFinder"


def _cases():
    import heapq
    import random
    rng = random.Random(74)
    out = []
    for adds in (25, 250_000):          # insort into a list is O(n) per add: too slow for 250,000
        ops, res, low, high, n = [("MedianFinder",)], [None], [], [], 0
        while n < adds:
            if n and rng.random() < 0.1:
                ops.append(("find_median",))
                res.append(float(-low[0]) if len(low) > len(high) else (-low[0] + high[0]) / 2)
            else:
                x = rng.randint(-10**5, 10**5)
                n += 1
                heapq.heappush(low, -x)
                heapq.heappush(high, -heapq.heappop(low))
                if len(high) > len(low):
                    heapq.heappush(low, -heapq.heappop(high))
                ops.append(("add_num", x))
                res.append(None)
        out.append((ops, res))
    return out


TEACHES = ["heap.two_heaps"]
USES = ["heap.max_negate"]

TESTS = [([("MedianFinder",), ("add_num", 1), ("add_num", 2), ("find_median",), ("add_num", 3), ("find_median",)],
          [None, None, None, 1.5, None, 2.0]),
         ([("MedianFinder",), ("add_num", -5), ("find_median",), ("add_num", -5), ("find_median",)],
          [None, None, -5.0, None, -5.0])] + _cases()
