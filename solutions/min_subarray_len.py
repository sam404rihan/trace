def min_subarray_len(target: int, nums: list[int]) -> int:
    # Variable window: grow right, shrink left WHILE the sum is still big enough.
    # Each index enters and leaves once, so O(n). (Only valid because nums > 0.)
    left = total = 0
    best = float("inf")
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best
