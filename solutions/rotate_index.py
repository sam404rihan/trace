def rotate_index(i: int, k: int, n: int) -> int:
    # Shift, then wrap. Python's % handles negative k and k > n for free.
    return (i + k) % n
