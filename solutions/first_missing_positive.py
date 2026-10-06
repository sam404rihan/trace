def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        # Send nums[i] to its home slot (value v lives at index v - 1) until this slot
        # holds something that can't move: out of range, or its home already has it.
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            home = nums[i] - 1
            nums[i], nums[home] = nums[home], nums[i]
    for k in range(n):
        if nums[k] != k + 1:
            return k + 1
    return n + 1
