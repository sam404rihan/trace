def extend_or_restart(cur: int, x: int) -> int:
    # A run with a negative sum never helps whatever comes next. Restart instead.
    return max(x, cur + x)
