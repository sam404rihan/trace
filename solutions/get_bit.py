def get_bit(x: int, k: int) -> int:
    return (x >> k) & 1     # slide bit k to the bottom, mask everything else away
