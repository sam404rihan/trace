def count_subarrays_median_k(nums: list[int], k: int) -> int:
    pos = nums.index(k)
    left = Counter({0: 1})          # balances of nums[i:pos] for every i <= pos (empty = 0)
    balance = 0
    for i in range(pos - 1, -1, -1):
        balance += 1 if nums[i] > k else -1
        left[balance] += 1
    total = balance = 0
    for j in range(pos, len(nums)):
        if j > pos:
            balance += 1 if nums[j] > k else -1
        # The whole subarray needs (#bigger - #smaller) to be 0 (odd length) or 1 (even length).
        total += left[-balance] + left[1 - balance]
    return total
