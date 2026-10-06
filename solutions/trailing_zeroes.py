def trailing_zeroes(n: int) -> int:
    count = 0
    while n:
        n //= 5             # how many multiples of 5, then of 25, then of 125, ...
        count += n
    return count
