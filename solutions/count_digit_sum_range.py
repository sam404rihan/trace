MOD = 1_000_000_007


def count_digit_sum_range(num1: str, num2: str, min_sum: int, max_sum: int) -> int:
    def count(bound):
        """x in [0, bound] whose digit sum is in [min_sum, max_sum]."""
        digits = [int(c) for c in bound]

        @cache
        def go(pos, total, tight):
            if total > max_sum:
                return 0                        # digits only add: it can't come back down
            if pos == len(digits):
                return 1 if total >= min_sum else 0
            limit = digits[pos] if tight else 9
            return sum(go(pos + 1, total + d, tight and d == limit) for d in range(limit + 1)) % MOD

        result = go(0, 0, True)
        go.cache_clear()
        return result

    first_ok = min_sum <= sum(map(int, num1)) <= max_sum
    return (count(num2) - count(num1) + first_ok) % MOD
