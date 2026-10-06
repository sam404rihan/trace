def lower_bound(nums: list[int], x: int) -> int:
    # Invariant: everything before lo is < x, everything from hi on is >= x.
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1        # mid and everything left of it is too small
        else:
            hi = mid            # mid might be the answer: keep it
    return lo                   # same as bisect.bisect_left(nums, x)
