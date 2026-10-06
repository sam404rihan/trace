def partition_k_subsets(nums: list[int], k: int) -> bool:
    total = sum(nums)
    if total % k or max(nums) > total // k:
        return False
    target, n = total // k, len(nums)
    fill = [-1] * (1 << n)          # fill[mask]: amount in the current (unfinished) group, or -1
    fill[0] = 0
    for mask in range(1 << n):
        if fill[mask] < 0:
            continue
        for i in range(n):
            if not mask >> i & 1 and fill[mask] + nums[i] <= target:
                fill[mask | 1 << i] = (fill[mask] + nums[i]) % target   # a full group rolls over to 0
    return fill[(1 << n) - 1] == 0
