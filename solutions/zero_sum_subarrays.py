def zero_sum_subarrays(nums: list[int]) -> int:
    # Equal running totals mark a zero-sum subarray between them. Count earlier copies. O(n).
    seen = {0: 1}                           # the empty start
    total = count = 0
    for x in nums:
        total += x
        count += seen.get(total, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
