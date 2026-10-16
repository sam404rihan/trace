def equal_pairs(nums: list[int]) -> int:
    # Each x pairs with every earlier x: add how many came before, then count this one. O(n).
    seen, pairs = {}, 0
    for x in nums:
        pairs += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return pairs
