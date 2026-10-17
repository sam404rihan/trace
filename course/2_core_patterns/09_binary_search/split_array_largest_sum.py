"""
Split Array Largest Sum                                                       [hard]

Split `nums` (non-negative integers) into exactly k non-empty contiguous parts
so that the largest part sum is as small as possible. Return that sum.
1 <= k <= len(nums).

Example:
    split_array_largest_sum([7, 2, 5, 10, 8], 2)   ->  18     [7, 2, 5] and [10, 8]
    split_array_largest_sum([1, 2, 3, 4, 5], 2)    ->  9      [1, 2, 3] and [4, 5]
    split_array_largest_sum([1, 4, 4], 3)          ->  4

Aim for:  O(n log(sum)) by binary searching on the answer.
Hint:     For a cap C, count how many parts a greedy pass needs: keep adding to the current part
          and start a new one when the next number would push it past C. More cap -> fewer
          parts, so search C between max(nums) and sum(nums) for the smallest C that needs <= k parts.
"""


def split_array_largest_sum(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    from functools import cache

    @cache
    def best(i, parts):
        if parts == 1:
            return sum(nums[i:])
        out, run = float("inf"), 0
        for j in range(i, len(nums) - parts + 1):
            run += nums[j]
            out = min(out, max(run, best(j + 1, parts - 1)))
        return out
    return best(0, k)


def _fast(nums, k):
    def parts(cap):
        count, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                count, cur = count + 1, 0
            cur += x
        return count
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if parts(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _cases():
    import random
    rng = random.Random(410)
    out = []
    for _ in range(10):
        nums = [rng.randint(0, 20) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, len(nums))
        out.append(((nums, k), _brute(nums, k)))
    big = [rng.randint(0, 10**6) for _ in range(50_000)]
    out.append(((big, 300), _fast(big, 300)))
    return out


USES = ["bsearch.first_true", "bsearch.on_answer"]

TESTS = [
    (([7, 2, 5, 10, 8], 2), 18),
    (([1, 2, 3, 4, 5], 2), 9),
    (([1, 4, 4], 3), 4),
    (([5], 1), 5),
    (([0, 0, 0], 2), 0),
    (([2, 3, 1, 2, 4, 3], 5), 4),
] + _cases()
