"""
Top K Frequent Elements                                  [medium] · arrays and hashing

Return the `k` most frequent values in `nums`, in any order.
The answer is guaranteed to be unique.

Example:
    top_k_frequent([1, 1, 1, 2, 2, 3], 2)  ->  [1, 2]

Aim for:  O(n log k) with a heap, or O(n) with "bucket sort"
Hint:     Count first. Then: a value can appear at most n times, so you could
          make a list of buckets where bucket[c] holds the values seen c times.
"""


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Any order is fine."""
    return sorted(got) == sorted(expected)


TESTS = [
    (([1, 1, 1, 2, 2, 3], 2), [1, 2]),
    (([1], 1), [1]),
    (([4, 4, 4, 5, 5, 6, 6, 6, 6], 2), [4, 6]),
    (([-1, -1], 1), [-1]),
    (([5, 3, 1, 1, 1, 3, 73, 1], 2), [1, 3]),
]
