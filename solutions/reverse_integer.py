def reverse_integer(x: int) -> int:
    sign = -1 if x < 0 else 1
    x, r = abs(x), 0
    while x:
        x, d = divmod(x, 10)
        r = r * 10 + d
    r *= sign
    return r if -2**31 <= r <= 2**31 - 1 else 0
