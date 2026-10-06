def max_product_subarray(nums: list[int]) -> int:
    best = high = low = nums[0]
    for x in nums[1:]:
        candidates = (x, high * x, low * x)     # a negative x swaps the roles of high and low
        high, low = max(candidates), min(candidates)
        best = max(best, high)
    return best
