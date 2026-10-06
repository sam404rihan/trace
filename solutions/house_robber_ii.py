def house_robber_ii(nums: list[int]) -> int:
    def rob_line(houses):
        two_back = one_back = 0
        for x in houses:
            two_back, one_back = one_back, max(one_back, two_back + x)
        return one_back

    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))   # never both ends
