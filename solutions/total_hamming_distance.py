def total_hamming_distance(nums: list[int]) -> int:
    n = len(nums)
    total = 0
    for bit in range(30):
        ones = sum(x >> bit & 1 for x in nums)
        total += ones * (n - ones)      # every (one, zero) pair differs at this bit
    return total
