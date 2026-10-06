"""
3Sum                                                         [medium] · two pointers

Return every unique triplet [a, b, c] of values from `nums` (different
positions) with a + b + c == 0. No duplicate triplets; any order.

Example:
    three_sum([-1, 0, 1, 2, -1, -4])  ->  [[-1, -1, 2], [-1, 0, 1]]

Aim for:  O(n²) time
Hint:     Sort first. Fix the first number, then find the other two with a
          left and a right pointer. Skip equal neighbours to avoid duplicates.
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Triplets, and the numbers inside them, may come back in any order."""
    def normalize(triplets):
        return sorted(sorted(t) for t in triplets)
    return normalize(got) == normalize(expected)


TESTS = [
    (([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]),
    (([0, 1, 1],), []),
    (([0, 0, 0],), [[0, 0, 0]]),
    (([0, 0, 0, 0],), [[0, 0, 0]]),
    (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]]),
]
