def house_robber(nums: list[int]) -> int:
    # best(i) = max(skip house i: best(i-1), rob it: best(i-2) + nums[i]).
    # Only the last two answers are needed: O(n) time, O(1) space.
    two_back = one_back = 0
    for x in nums:
        two_back, one_back = one_back, max(one_back, two_back + x)
    return one_back
