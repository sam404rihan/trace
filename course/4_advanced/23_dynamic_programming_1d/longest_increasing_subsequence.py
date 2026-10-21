"""
Longest Increasing Subsequence                                                [easy]

Return the length of the longest STRICTLY increasing subsequence of `nums`.
A subsequence keeps the order but can skip items.

Example:
    longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])  ->  4    [2, 3, 7, 18]

Aim for:  O(n log n). The last test has 100,000 numbers: the O(n²) DP (try it first) times out.
Hint:     dp[i] = length of the longest increasing subsequence ENDING at i
                = 1 + max(dp[j] for j < i if nums[j] < nums[i]), or 1.
          Faster: keep `tails`, where tails[k] is the smallest possible last
          value of an increasing run of length k + 1. For each x, replace
          tails[bisect_left(tails, x)] with x (or append it).
"""


def longest_increasing_subsequence(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(nums):
    from bisect import bisect_left
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def _big():
    import random
    rng = random.Random(2301)
    nums = [rng.randint(1, 10**9) for _ in range(100_000)]
    return (nums,), _fast(nums)


TEACHES = ["dp.lis"]
USES = ["bsearch.first_true"]

TESTS = [
    (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
    (([0, 1, 0, 3, 2, 3],), 4),
    (([7, 7, 7, 7],), 1),
    (([],), 0),
    (([4, 10, 4, 3, 8, 9],), 3),
    _big(),
]
