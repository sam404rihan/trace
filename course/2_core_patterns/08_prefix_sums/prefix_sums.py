"""
Build the prefix array                                                      [snippet]

Return P where P[k] is the sum of the first k numbers. P has one more entry
than nums, and P[0] = 0.

Example:
    prefix_sums([3, 1, 4])  ->  [0, 3, 4, 8]

Then sum(nums[i..j]) is just P[j + 1] - P[i]. You'll use that next.

Hint:     Start with [0] and append P[-1] + x for each x.
"""


def prefix_sums(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["prefix.sums"]
USES = []

TESTS = [
    (([3, 1, 4],), [0, 3, 4, 8]),
    (([],), [0]),
    (([5],), [0, 5]),
    (([2, -2, 2, -2],), [0, 2, 0, 2, 0]),
]
