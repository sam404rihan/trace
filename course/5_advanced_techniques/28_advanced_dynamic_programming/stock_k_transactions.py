"""
Best Time to Buy and Sell Stock IV                                              [hard]

Make at most k transactions (each one is a buy followed later by a sell), holding
at most one share at a time. Return the maximum profit.

Example:
    stock_k_transactions(2, [3, 2, 6, 5, 0, 3])  ->  7       buy 2 sell 6, buy 0 sell 3

Aim for:  O(n · k): a state machine with k layers.
Hint:     buy[j] = best balance while holding a share, during transaction j. sell[j] = best after
          finishing transaction j. For each price p, for j = 1..k:
          buy[j] = max(buy[j], sell[j-1] - p), and sell[j] = max(sell[j], buy[j] + p).
          (If k >= n // 2, it's the same as unlimited transactions.)
"""


def stock_k_transactions(k: int, prices: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(k, prices):
    from functools import lru_cache as memo

    @memo(None)
    def go(i, left, holding):
        if i == len(prices) or (left == 0 and not holding):
            return 0
        best = go(i + 1, left, holding)
        if holding:
            best = max(best, prices[i] + go(i + 1, left - 1, False))
        else:
            best = max(best, -prices[i] + go(i + 1, left, True))
        return best
    return go(0, k, False)


def _cases():
    import random
    rng = random.Random(308)
    out = []
    for _ in range(10):
        prices = [rng.randint(0, 12) for _ in range(rng.randint(0, 14))]
        k = rng.randint(0, 4)
        out.append(((k, prices), _brute(k, prices)))
    return out


TESTS = [((2, [3, 2, 6, 5, 0, 3]), 7), ((2, [2, 4, 1]), 2), ((0, [1, 5]), 0), ((1, [7, 6, 4, 3, 1]), 0),
         ((100, [1, 2, 1, 2, 1, 2]), 3)] + _cases()
