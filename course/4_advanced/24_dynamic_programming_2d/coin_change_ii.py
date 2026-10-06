"""
Coin Change II                                                                [medium]

Count the COMBINATIONS of coins (unlimited coins of each value) that add up to
amount. Order doesn't matter: 1 + 2 and 2 + 1 are the same combination.

Example:
    coin_change_ii(5, [1, 2, 5])  ->  4      5, 2+2+1, 2+1+1+1, 1+1+1+1+1
    coin_change_ii(3, [2])        ->  0

Aim for:  O(amount · coins).
Hint:     ways[0] = 1. Loop over COINS on the outside, amounts on the inside:
          ways[a] += ways[a - coin]. Swapping the loops counts orderings instead.
"""


def coin_change_ii(amount: int, coins: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(amount, coins):
    def go(i, left):
        if left == 0:
            return 1
        if i == len(coins):
            return 0
        return sum(go(i + 1, left - k * coins[i]) for k in range(left // coins[i] + 1))
    return go(0, amount)


def _make(rng):
    return (rng.randint(0, 25), rng.sample(range(1, 11), rng.randint(1, 4)))


def _cases():
    import random
    rng = random.Random(108)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [((5, [1, 2, 5]), 4), ((3, [2]), 0), ((10, [10]), 1), ((0, [7]), 1), ((500, [1, 2, 5, 10, 20, 50, 100, 200]), 6295434)] + _cases()
