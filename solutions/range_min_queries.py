def range_min_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    table = [nums[:]]                       # table[j][i] = min of nums[i : i + 2^j]
    j = 1
    while (1 << j) <= len(nums):
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(len(nums) - (1 << j) + 1)])
        j += 1
    out = []
    for l, r in queries:
        k = (r - l + 1).bit_length() - 1    # the biggest power of two that fits in the range
        out.append(min(table[k][l], table[k][r - (1 << k) + 1]))   # two overlapping blocks cover it
    return out
