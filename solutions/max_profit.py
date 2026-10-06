def max_profit(prices: list[int]) -> int:
    # Track the cheapest price so far; each day, try selling today. O(n), O(1).
    cheapest = float("inf")
    best = 0
    for price in prices:
        cheapest = min(cheapest, price)
        best = max(best, price - cheapest)
    return best
