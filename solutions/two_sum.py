def two_sum(nums: list[int], target: int) -> list[int]:
    # One pass with a hash map: value -> index. O(n) time, O(n) space.
    seen = {}
    for i, x in enumerate(nums):
        partner = target - x
        if partner in seen:          # O(1) average lookup
            return [seen[partner], i]
        seen[x] = i
    return []
