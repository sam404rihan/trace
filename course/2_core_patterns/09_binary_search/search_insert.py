"""
Search Insert Position                                                        [easy]

`nums` is sorted with distinct values. Return the index of `target` if it's
there, otherwise the index where it would be inserted to keep the order.

Example:
    search_insert([1, 3, 5, 6], 5)  ->  2
    search_insert([1, 3, 5, 6], 2)  ->  1

Aim for:  O(log n). Write the template yourself first, then compare with bisect.
Hint:     This is exactly "the first index where nums[i] >= target".
"""


def search_insert(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3, 5, 6], 5), 2),
    (([1, 3, 5, 6], 2), 1),
    (([1, 3, 5, 6], 7), 4),
    (([1, 3, 5, 6], 0), 0),
    (([], 3), 0),
]
