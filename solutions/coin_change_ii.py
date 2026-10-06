def coin_change_ii(amount: int, coins: list[int]) -> int:
    ways = [1] + [0] * amount
    for coin in coins:                      # coins outside: each combination counted once
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]
