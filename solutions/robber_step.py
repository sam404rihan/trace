def robber_step(prev2: int, prev1: int, x: int) -> int:
    # Skip this house (prev1), or rob it on top of the best that ended two houses back.
    return max(prev1, prev2 + x)
