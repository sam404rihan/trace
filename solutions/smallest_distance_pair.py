def smallest_distance_pair(nums: list[int], k: int) -> int:
    nums = sorted(nums)

    def pairs_within(d):
        """How many pairs have distance <= d (two pointers on the sorted list)."""
        count = left = 0
        for right in range(len(nums)):
            while nums[right] - nums[left] > d:
                left += 1
            count += right - left
        return count

    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if pairs_within(mid) >= k:      # the answer is mid or smaller
            hi = mid
        else:
            lo = mid + 1
    return lo
