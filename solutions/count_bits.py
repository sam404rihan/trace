def count_bits(n: int) -> list[int]:
    # i >> 1 drops the last bit, and we've already counted that smaller number. O(n).
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits

    # Built-in: [i.bit_count() for i in range(n + 1)]   (Python 3.10+)
