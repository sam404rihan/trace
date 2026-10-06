def min_jumps(nums: list[int]) -> int:
    # BFS in disguise: [start, end] is everything reachable with `jumps` jumps.
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])     # farthest reachable with one more jump
        if i == end:                    # finished this level: we have to jump
            jumps += 1
            end = far
    return jumps
