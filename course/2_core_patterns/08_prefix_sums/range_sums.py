"""
Range Sum Queries                                                             [easy]

For each query [l, r] in `queries`, return the sum of nums[l] through
nums[r] (inclusive). Return all the answers as a list.

Example:
    range_sums([1, 2, 3, 4, 5], [[0, 2], [1, 3]])  ->  [6, 9]

Aim for:  O(n + q). The last test has 20,000 queries over 100,000 numbers:
          summing each range from scratch will time out.
Hint:     Build prefix once: prefix = [0, *accumulate(nums)].
          Then each answer is prefix[r + 1] - prefix[l].
"""


def range_sums(nums: list[int], queries: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 2, 3, 4, 5], [[0, 2], [1, 3], [4, 4], [0, 4]]), [6, 9, 5, 15]),
    (([-2, 0, 3, -5, 2, -1], [[0, 2], [2, 5], [0, 5]]), [1, -1, -3]),
    (([7], [[0, 0]]), [7]),
    (([1] * 100_000, [[0, 99_999]] * 20_000), [100_000] * 20_000),
]
