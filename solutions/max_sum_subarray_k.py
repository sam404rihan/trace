def max_sum_subarray_k(nums: list[int], k: int) -> int:
    # Fixed window: add the number entering, subtract the one leaving. O(n).
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best
