"""
Numbers Without a Digit                                                       [guided]

Return how many integers x with 1 <= x <= n contain no digit d anywhere in their
decimal form (0 <= d <= 9).

Example:
    count_without_digit(20, 1)  ->  9        2..9 and 20 (1 and the 10s all contain a 1)
    count_without_digit(20, 0)  ->  18       10 and 20 are out
"""


def count_without_digit(n: int, d: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, d):
    return sum(1 for x in range(1, n + 1) if str(d) not in str(x))


def _dp(n, d):
    from functools import lru_cache
    digits = list(map(int, str(n)))

    @lru_cache(maxsize=None)
    def go(i, tight, started):
        if i == len(digits):
            return 1 if started else 0
        top = digits[i] if tight else 9
        total = 0
        for x in range(top + 1):
            now = started or x != 0
            if now and x == d:
                continue
            total += go(i + 1, tight and x == top, now)
        return total
    return go(0, True, False)


STEPS = [
    {
        "title": "Make it work",
        "text": "Loop over 1..n and test each number: str(d) not in str(x).",
        "hint": "sum(1 for x in range(1, n + 1) if str(d) not in str(x))",
        "tests": [((20, 1), 9), ((20, 0), 18), ((100, 5), 81), ((999, 9), _brute(999, 9)), ((1234, 3), _brute(1234, 3))],
    },
    {
        "title": "Edges",
        "text": "n smaller than 10, n = d itself, and d = 0, where leading zeros must not count (7 is fine, even though "
                "you could write it 007).",
        "hint": "If step 1 is right these pass. They pin down the leading-zero rule before you rewrite it.",
        "tests": [((1, 1), 0), ((1, 0), 1), ((9, 0), 9), ((5, 7), 5), ((10, 0), 9), ((100, 0), 90), ((7, 7), 6)],
    },
    {
        "title": "Make it fast: digit DP",
        "text": "n up to 10^18. Build the number digit by digit instead. State: (position, tight, started). tight means the "
                "prefix equals n's prefix, so the next digit is at most n's digit there; started means a non-zero digit has "
                "appeared, so zeros from now on are real digits. Skip any real digit equal to d. Memoise, and there are only "
                "about 19 × 2 × 2 states.",
        "hint": "@cache def go(i, tight, started): if i == len(s): return int(started). top = s[i] if tight else 9. For x in "
                "range(top + 1): now = started or x != 0; if now and x == d: continue; total += go(i + 1, tight and x == top, now).",
        "tests": [((n, d), _dp(n, d)) for n, d in ((10**18, 0), (10**18, 9), (987_654_321_987_654_321, 5),
                                                    (444_444_444_444_444_444, 4), (123_456_789_012_345_678, 1))],
    },
]
