def constrained_subset_sum(nums: list[int], k: int) -> int:
    dp = [0] * len(nums)
    window = deque()                            # indices with decreasing dp values
    for i, x in enumerate(nums):
        if window and window[0] < i - k:
            window.popleft()
        dp[i] = x + max(0, dp[window[0]] if window else 0)     # extend the best in reach, or start fresh
        while window and dp[window[-1]] <= dp[i]:
            window.pop()
        window.append(i)
    return max(dp)
