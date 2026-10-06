def at_most_n_given_digits(digits: list[str], n: int) -> int:
    s, k = str(n), len(digits)
    total = sum(k ** length for length in range(1, len(s)))     # every shorter number fits
    for i, ch in enumerate(s):
        rest = len(s) - i - 1
        total += sum(1 for d in digits if d < ch) * k ** rest   # smaller here: the rest is free
        if ch not in digits:
            return total                                        # can't match n's digit, so stop
    return total + 1                                            # n itself can be written
