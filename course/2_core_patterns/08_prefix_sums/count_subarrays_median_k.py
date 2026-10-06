"""
Count Subarrays With Median K                                                 [hard]

`nums` holds each of 1..n exactly once. Count the non-empty subarrays whose
median is k. The median of an odd-length list is its middle value once sorted.
For an even length it's the LEFT of the two middle values: the median of
[2, 3, 1, 4] is 2.

Example:
    count_subarrays_median_k([3, 2, 1, 4, 5], 4)  ->  3      [4], [4, 5], [1, 4, 5]
    count_subarrays_median_k([2, 3, 1], 3)        ->  1      just [3]

Aim for:  O(n).
Hint:     A subarray with median k must contain k. Replace each value by +1 (bigger than k) or
          -1 (smaller). The median is k exactly when the subarray has a balance of 0 or +1.
          Walk left from k's position and count each balance in a Counter. Then walk right
          from k: for a right balance b, add count[-b] + count[1 - b].
"""


def count_subarrays_median_k(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    total = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            s = sorted(nums[i:j + 1])
            total += s[(len(s) - 1) // 2] == k
    return total


def _fast(nums, k):
    p = nums.index(k)
    count, bal = {0: 1}, 0
    for i in range(p - 1, -1, -1):
        bal += 1 if nums[i] > k else -1
        count[bal] = count.get(bal, 0) + 1
    total, bal = 0, 0
    for j in range(p, len(nums)):
        if j > p:
            bal += 1 if nums[j] > k else -1
        total += count.get(-bal, 0) + count.get(1 - bal, 0)
    return total


def _cases():
    import random
    rng = random.Random(2488)
    out = []
    for _ in range(10):
        n = rng.randint(1, 12)
        nums = rng.sample(range(1, n + 1), n)
        k = rng.randint(1, n)
        out.append(((nums, k), _brute(nums, k)))
    big = list(range(1, 100_001))
    rng.shuffle(big)
    out.append(((big, 50_000), _fast(big, 50_000)))
    return out


TESTS = [
    (([3, 2, 1, 4, 5], 4), 3),
    (([2, 3, 1], 3), 1),
    (([1], 1), 1),
    (([1, 2], 1), 2),
    (([1, 2], 2), 1),
    (([2, 3, 1, 4], 2), 4),
] + _cases()
