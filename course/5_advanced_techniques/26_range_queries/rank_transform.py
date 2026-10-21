"""
Rank Transform of an Array                                                    [easy]

Replace every number with its rank: 1 for the smallest value, 2 for the next
smallest DIFFERENT value, and so on. Equal numbers get the same rank.

Example:
    rank_transform([40, 10, 20, 30, 10])  ->  [4, 1, 2, 3, 1]

Aim for:  O(n log n). The last test has 100,000 numbers: counting the smaller values
          for every number is O(n²) and times out.
Hint:     Sort the distinct values once: sorted(set(nums)). A dict from each value to its
          position + 1 is the rank table, and every number is then one lookup.
"""


def rank_transform(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(2601)
    nums = [rng.randint(-10**9, 10**9) for _ in range(100_000)]
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    return (nums,), [rank[x] for x in nums]


TEACHES = ["array.rank_compress"]
USES = []

TESTS = [
    (([40, 10, 20, 30, 10],), [4, 1, 2, 3, 1]),
    (([100, 100, 100],), [1, 1, 1]),
    (([],), []),
    (([7],), [1]),
    (([-5, 3, -5, 0],), [1, 3, 1, 2]),
    (([10**9, -10**9],), [2, 1]),
    _big(),
]
