"""
Target Sum                                                                    [medium]

Put a + or - in front of every number in nums. Count how many ways the
expression adds up to target.

Example:
    target_sum([1, 1, 1, 1, 1], 3)  ->  5

Aim for:  O(n · sum) with a dict of reachable totals, not 2^n.
Hint:     Keep counts: totals = {0: 1}. For each number x, every total t splits into t + x and t - x,
          carrying its count along. Read totals[target] at the end.
"""


def target_sum(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, target):
    n = len(nums)
    return sum(1 for m in range(1 << n) if sum(x if m >> i & 1 else -x for i, x in enumerate(nums)) == target)


def _make(rng):
    nums = [rng.randint(0, 5) for _ in range(rng.randint(1, 12))]
    return (nums, rng.randint(-sum(nums) - 1, sum(nums) + 1))


def _cases():
    import random
    rng = random.Random(109)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1), (([0, 0], 0), 4), (([2, 3], 7), 0), (([1] * 40, 0), 137846528820)] + _cases()
