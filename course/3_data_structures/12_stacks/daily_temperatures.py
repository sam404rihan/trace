"""
Daily Temperatures                                                  [medium] · stack

For each day, return how many days you have to wait until a warmer
temperature. Use 0 if no warmer day ever comes.

Example:
    daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
        ->  [1, 1, 4, 2, 1, 1, 0, 0]

Aim for:  O(n) time
Hint:     Keep a stack of days that are still waiting for a warmer day
          (a "monotonic stack"). Each new day may resolve several of them.
"""


def daily_temperatures(temps: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]),
    (([30, 40, 50, 60],), [1, 1, 1, 0]),
    (([30, 60, 90],), [1, 1, 0]),
    (([90, 80],), [0, 0]),
]
