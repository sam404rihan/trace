def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1          # drops exactly the lowest set bit
        count += 1
    return count
