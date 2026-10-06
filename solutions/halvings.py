def halvings(n: int) -> int:
    # Each loop halves n, so it runs about log2(n) times. (Also: n.bit_length() - 1.)
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps
