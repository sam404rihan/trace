"""
Longest Increasing Subsequence                                              [medium]

Return the length of the longest STRICTLY increasing subsequence of `nums`.
A subsequence keeps the order but can skip items.

Example:
    longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])  ->  4    [2, 3, 7, 18]

Aim for:  O(n²) DP first. Then the O(n log n) trick with bisect.
Hint:     dp[i] = length of the longest increasing subsequence ENDING at i
                = 1 + max(dp[j] for j < i if nums[j] < nums[i]), or 1.
          Faster: keep `tails`, where tails[k] is the smallest possible last
          value of an increasing run of length k + 1. For each x, replace
          tails[bisect_left(tails, x)] with x (or append it).
"""


def longest_increasing_subsequence(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
    (([0, 1, 0, 3, 2, 3],), 4),
    (([7, 7, 7, 7],), 1),
    (([],), 0),
    (([4, 10, 4, 3, 8, 9],), 3),
]
