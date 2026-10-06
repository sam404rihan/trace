class NumberRange:
    def __init__(self, lo: int, hi: int):
        self.lo, self.hi = lo, hi

    def _count(self, N, start, step, good):
        """How many x in [0, N] end in a good state. step(state, digit) returns the next state, or None to reject."""
        if N < 0:
            return 0
        digits = list(map(int, str(N)))

        @cache
        def go(i, tight, started, state):
            if i == len(digits):
                return 1 if good(state) else 0
            top = digits[i] if tight else 9
            total = 0
            for d in range(top + 1):
                now = started or d != 0
                nxt = step(state, d) if now else state        # leading zeros don't touch the state
                if nxt is not None:
                    total += go(i + 1, tight and d == top, now, nxt)
            return total

        return go(0, True, False, start)

    def _range(self, start, step, good):
        return self._count(self.hi, start, step, good) - self._count(self.lo - 1, start, step, good)

    def with_digit_sum(self, s: int) -> int:
        return self._range(0, lambda st, d: st + d if st + d <= s else None, lambda st: st == s)

    def digit_sum_divisible_by(self, k: int) -> int:
        return self._range(0, lambda st, d: (st + d) % k, lambda st: st == 0)

    def without_digit(self, d: int) -> int:
        return self._range(0, lambda st, x: None if x == d else 0, lambda st: True)

    def no_equal_neighbours(self) -> int:
        return self._range(-1, lambda prev, d: None if d == prev else d, lambda st: True)
