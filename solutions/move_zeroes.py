def move_zeroes(nums: list[int]) -> list[int]:
    # Write pointer: every non-zero is copied forward to nums[write]. O(n), O(1) space.
    write = 0
    for x in nums:
        if x != 0:
            nums[write] = x
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0
    return nums

    # Swap version (one loop): when nums[i] != 0, swap nums[i] with nums[write].
