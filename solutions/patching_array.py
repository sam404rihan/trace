def patching_array(nums: list[int], n: int) -> int:
    reach = 1               # every number in [1, reach) can be made so far
    patches = i = 0
    while reach <= n:
        if i < len(nums) and nums[i] <= reach:
            reach += nums[i]    # no gap: nums[i] extends the range to [1, reach + nums[i])
            i += 1
        else:
            reach += reach      # gap at reach: patching reach itself doubles the range
            patches += 1
    return patches
