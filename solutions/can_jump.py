def can_jump(nums: list[int]) -> bool:
    # Track the furthest index reachable so far. O(n), O(1).
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:               # we can't even stand here
            return False
        reach = max(reach, i + jump)
    return True
