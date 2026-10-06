"""
Sliding Window Median                                                         [hard]

Slide a window of size k across `nums` one step at a time and return the median
of every window, as floats. For an even k the median is the mean of the two
middle values.

Example:
    sliding_window_median([1, 3, -1, -3, 5, 3, 6, 7], 3)
        ->  [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    sliding_window_median([1, 2, 3, 4], 2)  ->  [1.5, 2.5, 3.5]

Aim for:  O(n log n). Sorting every window is O(n k log k): too slow for the big test.
Hint:     Two heaps, like the running median: a max-heap `low` and a min-heap `high`, with
          `low` holding the extra element when k is odd. Heaps can't delete from the middle, so
          delete lazily: count values that left the window in a dict, track how many VALID items
          each heap holds, and pop stale items only when they reach the top.
          (A sorted list with bisect.insort is a simpler O(n k) option that also passes.)
"""


def sliding_window_median(nums: list[int], k: int) -> list[float]:
    raise NotImplementedError  # replace this line with your solution


def _ref(nums, k):
    import bisect
    window = sorted(nums[:k])
    out = []
    for i in range(k, len(nums) + 1):
        mid = k // 2
        out.append(float(window[mid]) if k % 2 else (window[mid - 1] + window[mid]) / 2)
        if i < len(nums):
            window.pop(bisect.bisect_left(window, nums[i - k]))
            bisect.insort(window, nums[i])
    return out


def _cases():
    import random
    rng = random.Random(480)
    out = []
    for _ in range(10):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(1, 15))]
        k = rng.randint(1, len(nums))
        out.append(((nums, k), _ref(nums, k)))
    big = [rng.randint(-10**6, 10**6) for _ in range(30_000)]
    out.append(((big, 3_000), _ref(big, 3_000)))
    return out


TESTS = [
    (([1, 3, -1, -3, 5, 3, 6, 7], 3), [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]),
    (([1, 2, 3, 4], 2), [1.5, 2.5, 3.5]),
    (([5], 1), [5.0]),
    (([2, 2, 2, 2], 4), [2.0]),
    (([2147483647, 2147483647], 2), [2147483647.0]),
    (([1, 4, 2, 3], 4), [2.5]),
] + _cases()
