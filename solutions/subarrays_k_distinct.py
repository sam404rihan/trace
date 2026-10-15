def subarrays_k_distinct(nums: list[int], k: int) -> int:
    def at_most(k):
        count = Counter()
        left = total = 0
        for right, x in enumerate(nums):  #@skeleton
            count[x] += 1
            while len(count) > k:  #@skeleton
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1  #@skeleton
            total += right - left + 1       # every start in [left, right] works for this end
        return total

    return at_most(k) - at_most(k - 1)
