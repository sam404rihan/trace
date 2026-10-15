def min_ops_continuous(nums: list[int]) -> int:
    n = len(nums)
    vals = sorted(set(nums))        # duplicates must be changed anyway
    keep = left = 0
    for right, v in enumerate(vals):  #@skeleton
        while v - vals[left] > n - 1:       # the run starting at vals[left] can't reach v  #@skeleton
            left += 1  #@skeleton
        keep = max(keep, right - left + 1)
    return n - keep
