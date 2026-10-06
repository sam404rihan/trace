def slide_sum(window_sum: int, nums: list[int], right: int, k: int) -> int:
    # One in (nums[right]), one out (nums[right - k]). O(1) per step instead of O(k).
    return window_sum + nums[right] - nums[right - k]
