def contains_duplicate(nums: list[int]) -> bool:
    # A set answers "seen it?" in O(1). O(n) time, O(n) space.
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

    # One-liner: return len(set(nums)) < len(nums)
    # Space-free alternative: sort, then compare neighbours — O(n log n).
