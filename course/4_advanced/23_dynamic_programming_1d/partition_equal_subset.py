"""
Partition Equal Subset Sum                                                    [easy]

Can the positive integers in nums be split into two groups with equal sums?

Example:
    partition_equal_subset([1, 5, 11, 5])  ->  True       [1, 5, 5] and [11]
    partition_equal_subset([1, 2, 3, 5])   ->  False

Aim for:  O(n · sum). It's 0/1 knapsack: can some subset reach total / 2?
Hint:     An odd total means no. Otherwise keep the set (or a boolean array) of reachable sums. For
          each number x, every reachable s also makes s + x reachable. Loop s downwards so each
          number is used once.
"""


def partition_equal_subset(nums: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    total, n = sum(nums), len(nums)
    return total % 2 == 0 and any(sum(nums[i] for i in range(n) if m >> i & 1) * 2 == total for m in range(1 << n))


def _make(rng):
    return ([rng.randint(1, 12) for _ in range(rng.randint(1, 12))],)


def _cases():
    import random
    rng = random.Random(106)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TEACHES = ["dp.knapsack01"]
USES = []

TESTS = [(([1, 5, 11, 5],), True), (([1, 2, 3, 5],), False), (([2],), False), (([3, 3],), True),
         (([100] * 100 + [50, 50],), True)] + _cases()
