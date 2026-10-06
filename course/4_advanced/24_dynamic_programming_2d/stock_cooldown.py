"""
Best Time to Buy and Sell Stock with Cooldown                                 [medium]

prices[i] is the stock price on day i. You can make as many trades as you
like, holding at most one share at a time, but after you SELL you must wait one
day (cooldown) before buying again. Return the maximum profit.

Example:
    stock_cooldown([1, 2, 3, 0, 2])  ->  3      buy, sell, cooldown, buy, sell

Aim for:  O(n): a small state machine.
Hint:     Three states at the end of each day: holding a share, just sold (cooldown next), and
          resting (free to buy). holding = max(holding, resting - price), sold = holding + price,
          resting = max(resting, sold). Update them from the previous day's values.
"""


def stock_cooldown(prices: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(prices):
    from functools import lru_cache as memo

    @memo(None)
    def go(i, holding):
        if i >= len(prices):
            return 0
        skip = go(i + 1, holding)
        if holding:
            return max(skip, prices[i] + go(i + 2, False))
        return max(skip, -prices[i] + go(i + 1, True))
    return go(0, False)


def _make(rng):
    return ([rng.randint(0, 10) for _ in range(rng.randint(1, 14))],)


def _cases():
    import random
    rng = random.Random(107)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(([1, 2, 3, 0, 2],), 3), (([1],), 0), (([5, 4, 3],), 0), (([1, 4, 2],), 3), (([2, 1, 4],), 3)] + _cases()
