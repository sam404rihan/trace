"""
Combination Sum IV                                                            [medium]

Count the ORDERED sequences of numbers from nums (distinct, positive, reusable)
that add up to target. Different orders count as different sequences.

Example:
    combination_sum_iv([1, 2, 3], 4)  ->  7
        1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2, 1+3, 3+1

Aim for:  O(target · len(nums)).
Hint:     ways[t] = sum of ways[t - x] for each x <= t (the LAST number in the sequence is x).
          ways[0] = 1. Amounts on the outside, numbers inside, which counts orders. Compare that
          with Coin Change II, where swapping the loops counts combinations instead.
"""


def combination_sum_iv(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, target):
    if target == 0:
        return 1
    return sum(_brute(nums, target - x) for x in nums if x <= target)


def _cases():
    import random
    rng = random.Random(401)
    out = []
    for _ in range(8):
        nums = rng.sample(range(1, 8), rng.randint(1, 4))
        t = rng.randint(0, 12)
        out.append(((nums, t), _brute(nums, t)))
    return out


USES = ["dp.amounts"]

TESTS = [(([1, 2, 3], 4), 7), (([9], 3), 0), (([5], 0), 1), (([1, 2], 10), 89), (([2, 3, 5], 40), 560287)] + _cases()
