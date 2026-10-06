def count_pairs_below(nums: list[int], target: int) -> int:
    count, left, right = 0, 0, len(nums) - 1
    while left < right:
        if nums[left] + nums[right] < target:
            # nums[left] + anything in (left, right] is also below target: count them all at once.
            count += right - left
            left += 1
        else:
            right -= 1          # nums[right] is too big for every remaining partner
    return count
