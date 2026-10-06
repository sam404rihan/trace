def split_array_largest_sum(nums: list[int], k: int) -> int:
    def parts_needed(cap):
        parts, current = 1, 0
        for x in nums:
            if current + x > cap:       # x starts a new part
                parts += 1
                current = 0
            current += x
        return parts

    lo, hi = max(nums), sum(nums)       # a part must fit the biggest number; one part fits all
    while lo < hi:
        mid = (lo + hi) // 2
        if parts_needed(mid) <= k:      # fewer parts is fine: split one further, it only shrinks
            hi = mid
        else:
            lo = mid + 1
    return lo
