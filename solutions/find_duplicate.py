def find_duplicate(nums: list[int]) -> int:
    slow = fast = 0
    while True:                         # phase 1: meet somewhere inside the cycle
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0
    while slow != fast:                 # phase 2: meet again at the cycle's entrance
        slow, fast = nums[slow], nums[fast]
    return slow
