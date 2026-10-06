"""
Subarrays with K Different Integers                                           [hard]

Count the contiguous subarrays of `nums` that contain EXACTLY k different
values.

Example:
    subarrays_k_distinct([1, 2, 1, 2, 3], 2)  ->  7
        [1,2] [2,1] [1,2] [2,3] [1,2,1] [2,1,2] [1,2,1,2]
    subarrays_k_distinct([1, 2, 1, 3, 4], 3)  ->  3

Aim for:  O(n).
Hint:     "Exactly k" is awkward for a sliding window, but "at most k" is easy: for each right
          end, shrink the left until there are at most k distinct values, then every start from
          left to right works, adding right - left + 1. Exactly k = at_most(k) - at_most(k - 1).
"""


def subarrays_k_distinct(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    return sum(len(set(nums[i:j + 1])) == k for i in range(len(nums)) for j in range(i, len(nums)))


def _at_most(nums, k):
    count, left, total = {}, 0, 0
    for right, x in enumerate(nums):
        count[x] = count.get(x, 0) + 1
        while len(count) > k:
            count[nums[left]] -= 1
            if not count[nums[left]]:
                del count[nums[left]]
            left += 1
        total += right - left + 1
    return total


def _cases():
    import random
    rng = random.Random(992)
    out = []
    for _ in range(10):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(1, 14))]
        k = rng.randint(1, 4)
        out.append(((nums, k), _brute(nums, k)))
    big = [rng.randint(1, 50) for _ in range(100_000)]
    out.append(((big, 20), _at_most(big, 20) - _at_most(big, 19)))
    return out


TESTS = [
    (([1, 2, 1, 2, 3], 2), 7),
    (([1, 2, 1, 3, 4], 3), 3),
    (([1], 1), 1),
    (([1, 1, 1], 1), 6),
    (([1, 2], 3), 0),
] + _cases()
