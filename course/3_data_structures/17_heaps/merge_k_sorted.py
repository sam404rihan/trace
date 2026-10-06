"""
Merge K Sorted Lists                                                          [hard]

`lists` holds k lists, each sorted in ascending order. Merge them into one
sorted list.

Example:
    merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])  ->  [1, 1, 2, 3, 4, 4, 5, 6]

Aim for:  O(N log k), where N is the total number of items. Not
          sorted(sum(lists, [])): that ignores that the lists are already sorted.
Hint:     Put the first item of each list in a min-heap as (value, list_index,
          item_index). Pop the smallest, then push the next item from the same
          list. (Afterwards, compare with heapq.merge.)
"""


def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]),
    (([],), []),
    (([[]],), []),
    (([[5], [1], [3]],), [1, 3, 5]),
    (([[1, 2, 3], [], [0, 10]],), [0, 1, 2, 3, 10]),
]
