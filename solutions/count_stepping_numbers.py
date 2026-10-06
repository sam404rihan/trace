MOD = 1_000_000_007


def count_stepping_numbers(low: str, high: str) -> int:
    def count(bound):
        """Stepping numbers in [1, bound]."""
        digits = [int(c) for c in bound]

        @cache
        def go(pos, prev, tight, started):
            if pos == len(digits):
                return 1 if started else 0
            limit = digits[pos] if tight else 9
            total = 0
            for d in range(limit + 1):
                if started and abs(d - prev) != 1:
                    continue
                total += go(pos + 1, d, tight and d == limit, started or d != 0)
            return total % MOD

        result = go(0, 0, True, False)
        go.cache_clear()
        return result

    low_counts = all(abs(int(a) - int(b)) == 1 for a, b in zip(low, low[1:]))
    return (count(high) - count(low) + low_counts) % MOD
