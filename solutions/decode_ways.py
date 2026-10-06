MOD = 1_000_000_007


def decode_ways(s: str) -> int:
    # dp over prefixes, keeping only the last two values:
    # prev1 = ways to decode s[:i-1], prev2 = ways to decode s[:i-2]
    prev2, prev1 = 1, (0 if s[0] == "0" else 1)
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":                     # last letter used one digit
            cur += prev1
        if 10 <= int(s[i - 2:i]) <= 26:         # last letter used two digits
            cur += prev2
        prev2, prev1 = prev1, cur % MOD
    return prev1
