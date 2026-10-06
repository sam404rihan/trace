"""
Minimum Operations to Make Array Continuous                                   [hard]

An array is "continuous" when its values are all different and max - min equals
len - 1 (so it's some run like 4, 5, 6, 7 in any order). One operation replaces
any element with any integer. Return the fewest operations that make `nums`
continuous.

Example:
    min_ops_continuous([4, 2, 5, 3])       ->  0
    min_ops_continuous([1, 2, 3, 5, 6])    ->  1      change 6 to 4
    min_ops_continuous([1, 10, 100, 1000]) ->  3

Aim for:  O(n log n): sort once, then a sliding window.
Hint:     Keep as many elements as possible. If the final run starts at value v, you keep the
          distinct values inside [v, v + n - 1]. So sort the DISTINCT values and slide a window
          over them where right - left fits in that range. Answer = n - the biggest window.
"""


def min_ops_continuous(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    n, vals = len(nums), set(nums)
    return min(n - sum(v <= x <= v + n - 1 for x in vals) for v in vals)


def _cases():
    import random
    rng = random.Random(2009)
    out = []
    for _ in range(10):
        nums = [rng.randint(1, 15) for _ in range(rng.randint(1, 10))]
        out.append(((nums,), _brute(nums)))
    big = [rng.randint(1, 300_000) for _ in range(100_000)]
    vals = sorted(set(big))
    best, left = 0, 0
    for right in range(len(vals)):
        while vals[right] - vals[left] > len(big) - 1:
            left += 1
        best = max(best, right - left + 1)
    out.append(((big,), len(big) - best))
    return out


TESTS = [
    (([4, 2, 5, 3],), 0),
    (([1, 2, 3, 5, 6],), 1),
    (([1, 10, 100, 1000],), 3),
    (([7],), 0),
    (([5, 5, 5],), 2),
    (([8, 5, 9, 9, 8, 4],), 2),
] + _cases()
