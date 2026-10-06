"""
Combination Sum                                                             [medium]

`candidates` are distinct positive integers. Return every unique combination
that adds up to `target`. Each number can be used any number of times.
Combinations can be in any order; [2, 2, 3] and [3, 2, 2] count as the same one.

Example:
    combination_sum([2, 3, 6, 7], 7)  ->  [[2, 2, 3], [7]]

Aim for:  backtracking with pruning
Hint:     Sort first. explore(start, remaining): try candidates[i] for i >= start
          and recurse with i (not i + 1), since reuse is allowed. Break once a
          candidate is bigger than what remains.
"""


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Combinations, and the numbers inside them, may come back in any order."""
    def normalize(combos):
        return sorted(sorted(c) for c in combos)
    return normalize(got) == normalize(expected)


TESTS = [
    (([2, 3, 6, 7], 7), [[2, 2, 3], [7]]),
    (([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
    (([2], 1), []),
    (([1], 2), [[1, 1]]),
]
