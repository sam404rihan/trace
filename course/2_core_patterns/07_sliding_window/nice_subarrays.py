"""
Subarrays With k Odd Numbers                                                  [easy]

Count the contiguous subarrays of `nums` that hold exactly k odd numbers.
1 <= k <= len(nums).

Example:
    nice_subarrays([1, 1, 2, 1, 1], 3)  ->  2      [1, 1, 2, 1] and [1, 2, 1, 1]
    nice_subarrays([2, 4, 6], 1)        ->  0

Aim for:  O(n). The last test has 100,000 numbers: trying every start and end is
          O(n²) and times out.
Hint:     "At most k odd numbers" is easy with a window: for each right end, move
          left until the window holds at most k odds. Then every start from left
          to right works, so add right - left + 1. Exactly k is at_most(k) minus
          at_most(k - 1).
"""


def nice_subarrays(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["window.count"]
USES = ["window.variable"]

TESTS = [
    (([1, 1, 2, 1, 1], 3), 2),
    (([2, 4, 6], 1), 0),
    (([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2), 16),
    (([1], 1), 1),
    (([1, 1, 1], 1), 3),
    (([1, 1, 1], 3), 1),
    (([2, 1, 2], 1), 4),
    (([1 if i % 1000 == 0 else 2 for i in range(100_000)], 50), 50_001_000),
]
