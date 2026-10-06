def partition_equal_subset(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    half = total // 2
    reachable = [True] + [False] * half         # reachable[s]: some subset sums to s
    for x in nums:
        for s in range(half, x - 1, -1):        # downwards, so x is used at most once
            if reachable[s - x]:
                reachable[s] = True
    return reachable[half]
