"""
Constrained Subsequence Sum                                                     [hard]

Pick a non-empty subsequence of nums such that any two picked elements that are
neighbours in the subsequence are at most k apart in nums (j - i <= k). Return the
largest possible sum.

Example:
    constrained_subset_sum([10, 2, -10, 5, 20], 2)  ->  37       10 + 2 + 5 + 20
    constrained_subset_sum([-1, -2, -3], 1)         ->  -1       must pick at least one
    constrained_subset_sum([10, -2, -10, -5, 20], 2)  ->  23     10 - 2 - 5 + 20

Aim for:  O(n).
Hint:     dp[i] = the best sum of a valid subsequence ending at i
          = nums[i] + max(0, max(dp[i-k .. i-1])): either start fresh at i or extend the best
          one within reach. The window max is the same monotonic-deque trick as Jump Game VI.
          The answer is max(dp).
"""


def constrained_subset_sum(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(nums, k):
    from collections import deque
    dp, dq = [0] * len(nums), deque()
    for i, x in enumerate(nums):
        if dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = x + max(0, dp[dq[0]] if dq else 0)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return max(dp)


def _brute(nums, k):
    from itertools import combinations
    best = None
    n = len(nums)
    for r in range(1, n + 1):
        for idx in combinations(range(n), r):
            if all(b - a <= k for a, b in zip(idx, idx[1:])):
                s = sum(nums[i] for i in idx)
                best = s if best is None or s > best else best
    return best


def _cases():
    import random
    rng = random.Random(3404)
    out = []
    for _ in range(8):
        n = rng.randint(1, 11)
        nums = [rng.randint(-15, 15) for _ in range(n)]
        k = rng.randint(1, n)
        out.append(((nums, k), _brute(nums, k)))
    n = 100_000
    for k in (50_000, 3):
        nums = [rng.randint(-10_000, 9_000) for _ in range(n)]
        out.append(((nums, k), _ref(nums, k)))
    return out


USES = ["greedy.kadane", "deque.monotonic", "dp.recurrence"]

TESTS = [(([10, 2, -10, 5, 20], 2), 37), (([-1, -2, -3], 1), -1), (([10, -2, -10, -5, 20], 2), 23), (([7], 1), 7),
         (([-5, 3, -9, -9, 4], 2), _brute([-5, 3, -9, -9, 4], 2)), (([-5, 3, -9, -9, 4], 3), _brute([-5, 3, -9, -9, 4], 3))] + _cases()
