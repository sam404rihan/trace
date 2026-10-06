def get_sum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    a, b = a & mask, b & mask
    while b:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask    # sum without carry, then the carry
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)         # reinterpret as signed 32-bit
