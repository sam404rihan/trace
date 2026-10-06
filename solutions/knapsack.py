def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    # best[w] = most value within capacity w using the items processed so far.
    # Loop w DOWNWARDS so best[w - weight] still means "without this item":
    # each item is used at most once. O(n · capacity) time, O(capacity) space.
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            best[w] = max(best[w], best[w - weight] + value)
    return best[capacity]

    # Looping w upwards instead solves the "unbounded" knapsack (unlimited copies).
