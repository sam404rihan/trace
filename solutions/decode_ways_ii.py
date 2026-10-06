MOD = 1_000_000_007


def decode_ways_ii(s: str) -> int:
    def single(c):
        """How many letters one character can be."""
        return 9 if c == "*" else 0 if c == "0" else 1

    def pair(a, b):
        """How many letters the two characters a + b can be together (10..26)."""
        if a == "*" and b == "*":
            return 15                   # 11-19 and 21-26
        if a == "*":
            return 2 if b <= "6" else 1     # 1b and 2b, or only 1b
        if b == "*":
            return 9 if a == "1" else 6 if a == "2" else 0
        return 1 if 10 <= int(a + b) <= 26 else 0

    before, ways = 1, single(s[0])      # ways for s[:i-1] and s[:i]
    for i in range(1, len(s)):
        before, ways = ways, (single(s[i]) * ways + pair(s[i - 1], s[i]) * before) % MOD
    return ways
