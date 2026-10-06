"""
Find Median from Data Stream                                                    [hard]

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
    import bisect as _b
    import random
    rng = random.Random(74)
    out = []
    for size in (40, 150_000):
        ops, seen, res = [("MedianFinder",)], [], [None]
        for _ in range(size):
            if seen and rng.random() < 0.4:
                ops.append(("find_median",))
                n = len(seen)
                res.append(float(seen[n // 2]) if n % 2 else (seen[n // 2 - 1] + seen[n // 2]) / 2)
            else:
                x = rng.randint(-10**5, 10**5)
                ops.append(("add_num", x))
                _b.insort(seen, x)
                res.append(None)
        out.append((ops, res))
    return out


TESTS = [([("MedianFinder",), ("add_num", 1), ("add_num", 2), ("find_median",), ("add_num", 3), ("find_median",)],
          [None, None, None, 1.5, None, 2.0]),
         ([("MedianFinder",), ("add_num", -5), ("find_median",), ("add_num", -5), ("find_median",)],
          [None, None, -5.0, None, -5.0])] + _cases()
