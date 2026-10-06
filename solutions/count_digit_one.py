def count_digit_one(n: int) -> int:
    total, p = 0, 1
    while p <= n:
        high, cur, low = n // (p * 10), n // p % 10, n % p
        total += high * p                           # full cycles of 0..9 in this position
        if cur > 1:
            total += p                              # this cycle's 1s are all <= n
        elif cur == 1:
            total += low + 1                        # 1 followed by 0..low
        p *= 10
    return total
