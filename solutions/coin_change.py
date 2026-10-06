def coin_change(coins: list[int], amount: int) -> int:
    # best[x] = fewest coins that make x. Build up from 0. O(amount · len(coins)).
    INF = amount + 1                   # more coins than could ever be needed
    best = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and best[x - c] + 1 < best[x]:
                best[x] = best[x - c] + 1
    return best[amount] if best[amount] != INF else -1
