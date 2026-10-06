from bisect import bisect_left


def search_insert(nums: list[int], target: int) -> int:
    # "First index where nums[i] >= target" with the lo < hi template. O(log n).
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo

    # Shortcut: return bisect_left(nums, target)
