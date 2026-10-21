"""
Partition to K Equal Sum Subsets                                              [medium]

Can nums (positive) be split into exactly k non-empty groups with equal sums?

Example:
    partition_k_subsets([4, 3, 2, 3, 5, 2, 1], 4)  ->  True     (5) (1,4) (2,3) (2,3)
    partition_k_subsets([1, 2, 3, 4], 3)           ->  False

Aim for:  O(2^n · n) bitmask DP (n <= 16).
Hint:     target = total / k. Over masks of used numbers: fill[mask] = how much of the CURRENT group
          is filled (fill[mask] = -1 means unreachable). From a reachable mask, you can add any unused
          x with fill + x <= target, and the new fill is (fill + x) % target. True if the full mask is reachable.
"""


def partition_k_subsets(nums: list[int], k: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target, groups = total // k, [0] * k

    def place(i):
        if i == len(nums):
            return all(g == target for g in groups)
        tried = set()
        for g in range(k):
            if groups[g] + nums[i] <= target and groups[g] not in tried:
                tried.add(groups[g])
                groups[g] += nums[i]
                if place(i + 1):
                    return True
                groups[g] -= nums[i]
        return False
    return place(0)


def _cases():
    import random
    rng = random.Random(306)
    out = []
    for _ in range(10):
        nums = [rng.randint(1, 6) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, 4)
        out.append(((nums, k), _brute(nums, k)))
    return out


USES = ["bits.shift_mask", "dp.bitmask"]

TESTS = [(([4, 3, 2, 3, 5, 2, 1], 4), True), (([1, 2, 3, 4], 3), False), (([5], 1), True), (([2, 2, 2, 2, 3, 4, 5], 4), False),
         (([1] * 16, 8), True)] + _cases()
