def max_subarray(nums: list[int]) -> int:
    # Kadane: the best subarray ending at x either extends the previous one or
    # starts fresh at x. A negative running sum never helps, so drop it. O(n), O(1).
    best = current = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best
