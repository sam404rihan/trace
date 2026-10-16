"""
Count Bad Pairs                                                               [hard]

A pair of indices i < j is "bad" when j - i != nums[j] - nums[i].
Return how many bad pairs there are.

`nums` can hold 100,000 numbers, so checking every pair (about 5 billion of
them) is far too slow.

Example:
    count_bad_pairs([4, 1, 3, 3])     ->  5
        Only (1, 2) is good: 2 - 1 == 3 - 1. The other 5 of the 6 pairs are bad.
    count_bad_pairs([1, 2, 3, 4, 5])  ->  0

Aim for:  O(n).
Hint:     Rearrange: j - i == nums[j] - nums[i]  is the same as  nums[i] - i == nums[j] - j.
          So count the GOOD pairs instead: count how many indices share each nums[k] - k, in a dict.
          A group of size c has c * (c - 1) // 2 good pairs. Bad = all pairs - good pairs.
"""


def count_bad_pairs(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    n = len(nums)
    return sum(j - i != nums[j] - nums[i] for i in range(n) for j in range(i + 1, n))


def _fast(nums):
    seen, good = {}, 0
    for k, x in enumerate(nums):
        good += seen.get(x - k, 0)
        seen[x - k] = seen.get(x - k, 0) + 1
    return len(nums) * (len(nums) - 1) // 2 - good


def _cases():
    import random
    rng = random.Random(2364)
    out = []
    for _ in range(6):
        n = rng.randint(0, 30)
        start = rng.randint(-5, 5)
        nums = [start + k + rng.choice((0, 0, 0, 1, -1)) for k in range(n)]     # many good pairs
        out.append(((nums,), _brute(nums)))
    big = [k + rng.randint(0, 40) for k in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


USES = ["hash.count_pairs", "pairs.split_by_index"]

TESTS = [
    (([4, 1, 3, 3],), 5),
    (([1, 2, 3, 4, 5],), 0),
    (([],), 0),
    (([7],), 0),
    (([5, 5],), 1),
    (([3, 3, 3, 3],), 6),
] + _cases()
