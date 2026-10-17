def nice_subarrays(nums: list[int], k: int) -> int:
    def at_most(k):
        # For each right end, shrink until at most k odds; then every start in [left, right] works.
        left = odds = total = 0
        for right, x in enumerate(nums):
            odds += x % 2
            while odds > k:
                odds -= nums[left] % 2
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)      # exactly k = at most k minus at most k - 1
