def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    # Opposite-end pointers: each step rules out one number for good. O(n), O(1) space.
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1          # need a bigger sum
        else:
            right -= 1         # need a smaller sum
    return []
