def digit_sum(n: int) -> int:
    if n < 10:                          # base case: one digit
        return n
    return n % 10 + digit_sum(n // 10)  # last digit + (trusted) sum of the rest
