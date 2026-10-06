"""
Remove Duplicates from Sorted List                                            [easy]

`nums` is sorted. Remove the duplicates IN PLACE so each value appears once,
keeping the order. Then return the unique part: nums[:k].

Example:
    remove_duplicates_sorted([0, 0, 1, 1, 1, 2, 2, 3, 3, 4])  ->  [0, 1, 2, 3, 4]

Aim for:  O(n) time, O(1) extra space (so no set, no new list until the final slice)
Hint:     Slow and fast pointers. Because the list is sorted, a value is new
          exactly when it differs from the last value you kept.
"""


def remove_duplicates_sorted(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 1, 2],), [1, 2]),
    (([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],), [0, 1, 2, 3, 4]),
    (([],), []),
    (([5],), [5]),
    (([-3, -3, -3],), [-3]),
]
