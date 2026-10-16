"""
Best Time to Buy and Sell Stock                                               [easy]

`prices[i]` is a stock's price on day i. Buy on one day and sell on a later
day. Return the biggest profit you can make, or 0 if you can't profit.

Example:
    max_profit([7, 1, 5, 3, 6, 4])  ->  5      buy at 1, sell at 6

Aim for:  O(n) time, O(1) space
Hint:     Walk through the days once, remembering the cheapest price so far.
"""


def max_profit(prices: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([7, 1, 5, 3, 6, 4],), 5),
    (([7, 6, 4, 3, 1],), 0),
    (([2, 4, 1],), 2),
    (([1],), 0),
    (([3, 2, 6, 5, 0, 3],), 4),
]
