"""
Maximum Sum of k in a Row                                                     [easy]

Return the largest sum of any k consecutive numbers in `nums`.
(1 <= k <= len(nums))

Example:
    max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3)  ->  9      5 + 1 + 3

Aim for:  O(n). The last test has 200,000 numbers with k = 100,000: summing
          every window from scratch is O(n·k) and will time out.
Hint:     Fixed-size window: when it slides one step, one number enters and
          one leaves. Update the sum with just those two.
"""


def max_sum_subarray_k(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["window.fixed"]

TESTS = [
    (([2, 1, 5, 1, 3, 2], 3), 9),
    (([2, 3, 4, 1, 5], 2), 7),
    (([5], 1), 5),
    (([-1, -2, -3], 2), -3),
    ((list(range(200_000)), 100_000), sum(range(100_000, 200_000))),
]
