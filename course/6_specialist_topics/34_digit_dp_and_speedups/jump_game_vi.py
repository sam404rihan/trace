"""
Jump Game VI                                                                  [medium]

You start on index 0 of nums and want to reach the last index. From index i you may
jump forward to any of i + 1 .. i + k. Your score is the sum of nums at every index you
land on, including the first and the last. Return the highest possible score.

Example:
    jump_game_vi([1, -1, -2, 4, -7, 3], 2)  ->  7         1 → -1 → 4 → 3
    jump_game_vi([10, -5, -2, 4, 0, 3], 3)  ->  17        10 → 4 → 3

Aim for:  O(n). The last test has n = 100,000 and k = 50,000, so scanning the window
          for every i is billions of steps.
Hint:     dp[i] = nums[i] + max(dp[i-k .. i-1]). Keep a deque of indices whose dp values decrease
          from front to back. The front is the window's max: drop it once it is out of reach
          (index < i - k). Before appending i, pop from the back every index whose dp <= dp[i];
          they can never be the max again.
"""


def jump_game_vi(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(nums, k):
    from collections import deque
    dp, dq = [0] * len(nums), deque()
    for i, x in enumerate(nums):
        if dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = x + (dp[dq[0]] if dq else 0)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[-1]


def _brute(nums, k):
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        dp[i] = nums[i] + max(dp[max(0, i - k):i])
    return dp[-1]


def _cases():
    import random
    rng = random.Random(3403)
    out = []
    for _ in range(8):
        n = rng.randint(1, 30)
        nums = [rng.randint(-20, 20) for _ in range(n)]
        k = rng.randint(1, n)
        out.append(((nums, k), _brute(nums, k)))
    n = 100_000
    nums = [rng.randint(-10_000, 10_000) for _ in range(n)]
    out.append(((nums, 50_000), _ref(nums, 50_000)))
    nums = list(range(n, 0, -1))
    out.append(((nums, 40_000), _ref(nums, 40_000)))
    return out


USES = ["deque.monotonic", "dp.recurrence"]

TESTS = [(([1, -1, -2, 4, -7, 3], 2), 7), (([10, -5, -2, 4, 0, 3], 3), 17), (([1, -5, -20, 4, -1, 3, -6, -3], 2), 0),
         (([5], 1), 5), (([-1, -2, -3], 1), -6), (([-1, -2, -3], 2), -4)] + _cases()
