def binary_search(nums: list[int], target: int) -> int:
    # Invariant: if target is present, it's inside nums[lo..hi] (inclusive).
    # `lo <= hi` because a one-element range (lo == hi) still needs checking.
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1           # target is right of mid
        else:
            hi = mid - 1           # target is left of mid
    return -1

    # Standard library: bisect.bisect_left(nums, target) gives the insert position.
