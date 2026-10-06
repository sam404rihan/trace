def jump_game_vi(nums: list[int], k: int) -> int:
    dp = [0] * len(nums)
    window = deque()                            # indices, dp values decreasing front to back
    for i, x in enumerate(nums):
        if window and window[0] < i - k:
            window.popleft()                    # too far back to jump from
        dp[i] = x + (dp[window[0]] if window else 0)
        while window and dp[window[-1]] <= dp[i]:
            window.pop()                        # i is newer and at least as good
        window.append(i)
    return dp[-1]
