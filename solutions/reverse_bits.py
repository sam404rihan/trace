def reverse_bits(x: int, width: int) -> int:
    result = 0
    for _ in range(width):
        result = (result << 1) | (x & 1)    # push x's lowest bit onto the result
        x >>= 1                              # and peel it off x
    return result
