from collections import Counter


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    # A subarray (i, j] sums to k exactly when prefix[i] == prefix[j] - k.
    # Count earlier prefixes as we go. O(n), and negatives are fine.
    seen = Counter({0: 1})      # the empty prefix, for subarrays starting at index 0
    total = count = 0
    for x in nums:
        total += x
        count += seen[total - k]
        seen[total] += 1
    return count
