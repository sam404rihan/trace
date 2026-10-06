def stock_cooldown(prices: list[int]) -> int:
    holding, sold, resting = float("-inf"), 0, 0
    for p in prices:
        # yesterday's three states feed today's
        holding, sold, resting = max(holding, resting - p), holding + p, max(resting, sold)
    return max(sold, resting)
