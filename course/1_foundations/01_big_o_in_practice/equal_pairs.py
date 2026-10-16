"""
Matching Pairs                                                                [easy]

Count the pairs of indexes i < j where nums[i] == nums[j].

`nums` can hold 100,000 numbers, so checking every pair is far too slow.

Example:
    equal_pairs([1, 2, 3, 1, 1, 3])  ->  4      (0, 3), (0, 4), (3, 4) and (2, 5)

Aim for:  O(n), one pass.
Hint:     Walk the list once with a dict of how many times you've seen each value so far.
          A new x makes a pair with every earlier x: add seen[x] to the answer, then add 1
          to seen[x].
"""


def equal_pairs(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["hash.count_pairs"]
USES = []

TESTS = [
    (([1, 2, 3, 1, 1, 3],), 4),
    (([1, 1, 1, 1],), 6),
    (([1, 2, 3],), 0),
    (([],), 0),
    (([5],), 0),
    (([2, 2],), 1),
    (([-1, 3, -1, 3, -1],), 4),
    (([k % 1000 for k in range(100_000)],), 4_950_000),
]
