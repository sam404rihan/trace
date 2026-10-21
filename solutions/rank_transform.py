def rank_transform(nums: list[int]) -> list[int]:
    # Sort the distinct values once; each value's rank is its position there + 1. O(n log n).
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    return [rank[x] for x in nums]
