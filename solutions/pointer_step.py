def pointer_step(nums: list[int], left: int, right: int, target: int) -> tuple[int, int]:
    total = nums[left] + nums[right]
    if total < target:
        return left + 1, right      # nums[left] is too small even with the biggest partner left
    if total > target:
        return left, right - 1      # nums[right] is too big even with the smallest partner left
    return left, right
