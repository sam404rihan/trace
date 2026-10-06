def stock_k_transactions(k: int, prices: list[int]) -> int:
    if k == 0 or not prices:
        return 0
    buy = [float("-inf")] * (k + 1)     # buy[j]: best balance holding a share in transaction j
    sell = [0] * (k + 1)                # sell[j]: best balance after completing j transactions
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
