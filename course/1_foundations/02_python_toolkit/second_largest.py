"""
Second Largest                                                                [easy]

Return the second largest DISTINCT value in `nums`, or None if there
isn't one.

Example:
    second_largest([3, 1, 4, 1, 5])  ->  4
    second_largest([7, 7, 7])        ->  None

Aim for:  O(n) with one pass. The quick version is fine too: sorted(set(nums)).
Hint:     Track `best` and `second` as you go, starting both at float("-inf").
          When a number beats `best`, the old best becomes `second`.
"""


def second_largest(nums: list[int]) -> int | None:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([3, 1, 4, 1, 5],), 4),
    (([7, 7, 7],), None),
    (([2, 9],), 2),
    (([5],), None),
    (([-1, -2, -3],), -2),
    (([5, 5, 4],), 4),
]
