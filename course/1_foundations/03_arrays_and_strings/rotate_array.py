"""
Rotate Array                                                                [medium]

Rotate `nums` to the right by `k` steps and return it. `k` can be larger
than the length of the list.

Example:
    rotate_array([1, 2, 3, 4, 5, 6, 7], 3)  ->  [5, 6, 7, 1, 2, 3, 4]

Aim for:  O(n). First the slicing version, then try O(1) extra space.
Hint:     k %= len(nums) handles big k. Slicing: nums[-k:] + nums[:-k].
          O(1) space trick: reverse the whole list, then reverse the first k
          items, then reverse the rest.
"""


def rotate_array(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]),
    (([-1, -100, 3, 99], 2), [3, 99, -1, -100]),
    (([1, 2], 3), [2, 1]),
    (([1], 0), [1]),
    (([1, 2, 3], 3), [1, 2, 3]),
]
