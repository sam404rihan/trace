from collections import deque


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    # Monotonic deque of indexes, values decreasing front to back.
    # A smaller value behind a bigger, newer one can never be a max again: drop it.
    # Each index enters and leaves once, so O(n).
    dq, result = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:               # the front slid out of the window
            dq.popleft()
        if i >= k - 1:                   # the first full window ends at k - 1
            result.append(nums[dq[0]])
    return result
