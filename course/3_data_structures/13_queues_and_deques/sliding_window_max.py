"""
Sliding Window Maximum                                                        [hard]

A window of size k slides across `nums` one step at a time. Return the
maximum of each window.

Example:
    sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)  ->  [3, 3, 5, 5, 6, 7]

Aim for:  O(n). The last test has 100,000 numbers and k = 50,000, so calling
          max() on every window (O(n·k)) will time out.
Hint:     Monotonic deque of INDEXES with decreasing values. Pop smaller
          values off the back before adding; pop the front when it leaves
          the window. The front is always the current max.
"""


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
    (([1], 1), [1]),
    (([9, 8, 7, 6], 2), [9, 8, 7]),
    (([1, 2, 3, 4], 4), [4]),
    ((list(range(100_000)), 50_000), list(range(49_999, 100_000))),
]
