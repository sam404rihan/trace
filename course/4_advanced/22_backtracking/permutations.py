"""
Permutations                                                 [medium] · backtracking

`nums` has distinct values. Return every ordering of them, in any order.
(No itertools — the point is to write the backtracking yourself.)

Example:
    permutations([1, 2, 3])
        ->  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

Aim for:  O(n · n!) time
Hint:     Build a path one slot at a time. At each step try every number that
          isn't used yet, recurse, then undo the choice ("backtrack").
"""


def permutations(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """The permutations may come back in any order."""
    return sorted(map(list, got)) == sorted(expected)


TESTS = [
    (([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
    (([0, 1],), [[0, 1], [1, 0]]),
    (([1],), [[1]]),
]
