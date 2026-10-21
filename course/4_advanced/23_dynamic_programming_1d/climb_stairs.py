"""
Climbing Stairs                                             [easy] · dynamic programming

You're climbing a staircase with `n` steps. Each move you climb 1 or 2 steps.
In how many distinct ways can you reach the top?

Example:
    climb_stairs(3)  ->  3      1+1+1, 1+2, 2+1

Aim for:  O(n) time, O(1) space
Hint:     To land on step n, your last move came from step n-1 or step n-2.
          The obvious recursion is correct but exponential — the last test
          WILL time out. Fix it with memoisation (functools.cache), then with a
          bottom-up loop that only keeps the last two answers.
"""


def climb_stairs(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["recursion.memo", "dp.recurrence"]

TESTS = [
    ((1,), 1),
    ((2,), 2),
    ((3,), 3),
    ((5,), 8),
    ((10,), 89),
    ((45,), 1836311903),
]
