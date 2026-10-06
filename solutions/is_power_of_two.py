def is_power_of_two(n: int) -> bool:
    # A power of two is a single 1 bit; n & (n - 1) clears the lowest 1 bit. O(1).
    return n > 0 and n & (n - 1) == 0

    # Also works: n > 0 and n.bit_count() == 1
