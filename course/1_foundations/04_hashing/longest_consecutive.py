"""
Longest consecutive run                                                      [guided]

Given unsorted integers, return the length of the longest run of consecutive
values (like 4, 5, 6, 7) that can be formed from them. Order in the list
doesn't matter.

Example:
    longest_consecutive([100, 4, 200, 1, 3, 2])  ->  4      (1, 2, 3, 4)
"""


def longest_consecutive(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(5)
    nums = rng.sample(range(-10**9, 10**9), 60_000)
    start = 123_456
    nums += list(range(start, start + 40_000))
    rng.shuffle(nums)
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 not in present:
            y = x
            while y in present:
                y += 1
            best = max(best, y - x)
    return nums, best


_NUMS, _BEST = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Put the numbers in a set. For each number, count upward (x, x+1, x+2…) while the next value is in the set.",
        "hint": "Membership in a set is O(1), so asking 'is x + 1 here?' is cheap.",
        "tests": [
            (([100, 4, 200, 1, 3, 2],), 4),
            (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9),
            (([10, 30, 20],), 1),
        ],
    },
    {
        "title": "Edges",
        "text": "Empty input, duplicates, negative numbers.",
        "hint": "An empty list has no run: 0. Duplicates don't extend a run, and a set removes them anyway.",
        "tests": [
            (([],), 0),
            (([1, 2, 2, 3],), 3),
            (([-3, -1, -2, 5],), 3),
            (([9],), 1),
        ],
    },
    {
        "title": "Make it fast",
        "text": "100,000 numbers, including one run 40,000 long. If you count upward from every number in that run, "
                "you redo the same run again and again: O(n²). Only start counting where a run begins.",
        "hint": "x starts a run only if x - 1 is not in the set. Then every number is visited at most twice: O(n).",
        "tests": [
            (([5, 4, 3, 2, 1],), 5),
            ((_NUMS,), _BEST),
        ],
    },
]
