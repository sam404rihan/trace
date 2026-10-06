"""
Coin Change                                               [medium] · dynamic programming

Given coin denominations `coins` (unlimited supply of each) and an `amount`,
return the fewest coins that add up to exactly `amount`, or -1 if it can't
be done.

Example:
    coin_change([1, 2, 5], 11)  ->  3      5 + 5 + 1
    coin_change([2], 3)         ->  -1

Aim for:  O(amount · len(coins)) time
Hint:     Greedy (always take the biggest coin) fails — see the [1, 3, 4] test.
          Let best[x] = fewest coins for amount x. Then
          best[x] = 1 + min(best[x - c] for each coin c that fits).
"""


def coin_change(coins: list[int], amount: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 2, 5], 11), 3),
    (([2], 3), -1),
    (([1], 0), 0),
    (([1, 3, 4], 6), 2),
    (([186, 419, 83, 408], 6249), 20),
]
