def pivot_index(nums: list[int]) -> int:
    # right side = total - left side - the pivot itself. O(n), O(1) space.
    total = sum(nums)
    left_sum = 0
    for i, x in enumerate(nums):
        if left_sum == total - left_sum - x:
            return i
        left_sum += x
    return -1
