"""
Number range explorer                                                          [build]

A lottery analyst wants statistics about every ticket number in a range [lo, hi]
(1 <= lo <= hi <= 10^18), without looping over a quintillion tickets.

    r = NumberRange(1, 100)
    r.with_digit_sum(10)          ->  9          19, 28, 37, 46, 55, 64, 73, 82, 91
    r.digit_sum_divisible_by(5)   ->  19         5, 14, 19, 23, ..., 91, 96, 100
    r.without_digit(0)            ->  90         1..9 and 11..99 without 0s
    r.no_equal_neighbours()       ->  90         everything except 11, 22, ..., 99 and 100

Rules:
  - with_digit_sum(s): how many x in [lo, hi] have digit sum exactly s.
  - digit_sum_divisible_by(k): how many have digit sum divisible by k (1 <= k <= 100).
  - without_digit(d): how many contain no digit d (leading zeros don't count).
  - no_equal_neighbours(): how many have no two equal adjacent digits.

Aim for:  each question in O(19 · state · 10). The last test asks 30 questions about ranges
          up to 10^18.
Hint:     Write count(N) for [0, N] and answer count(hi) - count(lo - 1). All four are the
          same digit DP with a different extra state: the digit sum (or the sum mod k), a
          "started" flag for leading zeros, and the previous digit (with started, since a
          leading zero isn't a neighbour). One helper that takes the transition as a function
          keeps the four methods short.
"""


class NumberRange:
    def __init__(self, lo: int, hi: int):
        raise NotImplementedError

    def with_digit_sum(self, s: int) -> int:
        raise NotImplementedError

    def digit_sum_divisible_by(self, k: int) -> int:
        raise NotImplementedError

    def without_digit(self, d: int) -> int:
        raise NotImplementedError

    def no_equal_neighbours(self) -> int:
        raise NotImplementedError


CLASS = "NumberRange"


def _count(N, start, step, good):
    """How many x in [0, N] end in a good state. step(state, digit, started_before) -> state or None (reject)."""
    from functools import lru_cache
    if N < 0:
        return 0
    digits = list(map(int, str(N)))

    @lru_cache(maxsize=None)
    def go(i, tight, started, state):
        if i == len(digits):
            return 1 if good(state, started) else 0
        top = digits[i] if tight else 9
        total = 0
        for d in range(top + 1):
            now = started or d != 0
            nxt = step(state, d, now) if now else state
            if nxt is None:
                continue
            total += go(i + 1, tight and d == top, now, nxt)
        return total
    return go(0, True, False, start)


def _ask(lo, hi, op, arg):
    if op == "with_digit_sum":
        f = lambda N: _count(N, 0, lambda st, d, now: st + d if st + d <= arg else None, lambda st, started: st == arg)
    elif op == "digit_sum_divisible_by":
        f = lambda N: _count(N, 0, lambda st, d, now: (st + d) % arg, lambda st, started: st == 0)
    elif op == "without_digit":
        f = lambda N: _count(N, 0, lambda st, d, now: None if d == arg else 0, lambda st, started: True)
    else:
        f = lambda N: _count(N, -1, lambda st, d, now: None if d == st else d, lambda st, started: True)
    return f(hi) - f(lo - 1)


def _brute(lo, hi, op, arg):
    def ok(x):
        s = str(x)
        if op == "with_digit_sum":
            return sum(map(int, s)) == arg
        if op == "digit_sum_divisible_by":
            return sum(map(int, s)) % arg == 0
        if op == "without_digit":
            return str(arg) not in s
        return all(a != b for a, b in zip(s, s[1:]))
    return sum(1 for x in range(lo, hi + 1) if ok(x))


def _query(rng, big):
    op = rng.choice(["with_digit_sum", "digit_sum_divisible_by", "without_digit", "no_equal_neighbours"])
    arg = {"with_digit_sum": rng.randint(0, 120 if big else 30), "digit_sum_divisible_by": rng.randint(1, 60 if big else 12),
           "without_digit": rng.randint(0, 9), "no_equal_neighbours": None}[op]
    return op, arg


def _session(seed, lo, hi, q, big):
    import random
    rng = random.Random(seed)
    calls, want = [("NumberRange", lo, hi)], [None]
    for _ in range(q):
        op, arg = _query(rng, big)
        calls.append((op,) if arg is None else (op, arg))
        want.append(_ask(lo, hi, op, arg) if big else _brute(lo, hi, op, arg))
    return calls, want


TESTS = [([("NumberRange", 1, 100), ("with_digit_sum", 10), ("digit_sum_divisible_by", 5), ("without_digit", 0),
           ("no_equal_neighbours",)], [None, 9, 19, 90, 90]),
         ([("NumberRange", 7, 7), ("with_digit_sum", 7), ("without_digit", 7), ("no_equal_neighbours",), ("digit_sum_divisible_by", 1)],
          [None, 1, 0, 1, 1]),
         _session(3405, 1, 999, 12, False), _session(3406, 345, 4321, 12, False), _session(3407, 1000, 1000, 6, False),
         _session(3408, 10**17 + 12_345, 10**18, 15, True), _session(3409, 1, 987_654_321_987_654_321 // 10, 15, True)]
