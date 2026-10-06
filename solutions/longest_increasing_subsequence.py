from bisect import bisect_left


def longest_increasing_subsequence(nums: list[int]) -> int:
    # O(n log n) "patience" method. tails[k] = smallest possible last value of an
    # increasing subsequence of length k + 1. tails stays sorted, so binary search it.
    tails = []
    for x in nums:
        i = bisect_left(tails, x)        # bisect_left keeps it STRICTLY increasing
        if i == len(tails):
            tails.append(x)              # x extends the longest run
        else:
            tails[i] = x                 # x is a smaller ending for runs of length i + 1
    return len(tails)


def lis_quadratic(nums: list[int]) -> int:
    # The classic O(n²) DP: dp[i] = longest increasing subsequence ending at i.
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)
