"""
Subsets                                                                       [easy]

`nums` has distinct values. Return every possible subset (the "power set"),
including the empty one. Any order.

Example:
    subsets([1, 2, 3])
        ->  [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

Aim for:  O(n · 2ⁿ) time — there are 2ⁿ subsets, so you can't do better
Hint:     For each number you make one choice: take it or leave it.
          Recurse on the rest, and append a COPY of your current path
          (path[:]) when you reach the end.
"""


def subsets(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Subsets, and the numbers inside them, may come back in any order."""
    def normalize(sets):
        return sorted(sorted(s) for s in sets)
    return normalize(got) == normalize(expected)


USES = ["bt.core"]

TESTS = [
    (([1, 2, 3],), [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]),
    (([0],), [[], [0]]),
    (([],), [[]]),
]
