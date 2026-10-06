def count_without_digit(n: int, d: int) -> int:
    digits = list(map(int, str(n)))

    @cache
    def go(i, tight, started):
        if i == len(digits):
            return 1 if started else 0              # 0 itself isn't in the range
        top = digits[i] if tight else 9
        total = 0
        for x in range(top + 1):
            now = started or x != 0                 # leading zeros aren't digits of the number
            if now and x == d:
                continue
            total += go(i + 1, tight and x == top, now)
        return total

    return go(0, True, False)
