"""
Decode a message                                                             [guided]

Letters were encoded as numbers: A = 1, B = 2, …, Z = 26, and then the
numbers were written together with no spaces. Given the digit string, count
how many different letter messages it could have come from. The count can be
huge, so return it modulo 1_000_000_007.

Example:
    decode_ways("226")  ->  3      "BZ" (2 26), "VF" (22 6), "BBF" (2 2 6)

`s` is never empty.
"""

MOD = 1_000_000_007


def decode_ways(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ways(s):
    prev2, prev1 = 1, (0 if s[0] == "0" else 1)
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += prev1
        if s[i - 2] == "1" or (s[i - 2] == "2" and s[i - 1] <= "6"):
            cur += prev2
        prev2, prev1 = prev1, cur % MOD
    return prev1 % MOD


def _big():
    import random
    rng = random.Random(30)
    s = "".join(rng.choice("1112226") for _ in range(4000))
    return s, _ways(s)


_LONG, _LONG_WAYS = _big()

STEPS = [
    {
        "title": "Recurse on the first choice",
        "text": "These strings have no zeros. The first letter uses either one digit or two (if those two make 10..26). "
                "So ways(s) = ways(s[1:]) + ways(s[2:]) when the first two digits make a valid letter.",
        "hint": "Base case: the empty rest counts as 1 way (you've decoded everything). Work with an index i instead of slicing.",
        "tests": [
            (("12",), 2),
            (("226",), 3),
            (("1111111111",), 89),
            (("27",), 1),
        ],
    },
    {
        "title": "Zeros",
        "text": "0 is not a letter. A single-digit step can't use \"0\", and a two-digit step can't start with \"0\" "
                "(\"06\" isn't 6). Only \"10\" and \"20\" can absorb a zero.",
        "hint": "Single step: allowed if s[i] != '0'. Double step: allowed if 10 <= int(s[i:i+2]) <= 26.",
        "tests": [
            (("10",), 1),
            (("06",), 0),
            (("0",), 0),
            (("2101",), 1),
            (("11106",), 2),
            (("30",), 0),
        ],
    },
    {
        "title": "4,000 digits",
        "text": "The recursion branches twice per digit, so a 4,000-digit message has astronomically many calls. "
                "But ways(i) only depends on ways(i + 1) and ways(i + 2): memoise it, or fill an array from the end "
                "(or from the start, with dp[i] = ways to decode the first i digits). Remember % MOD.",
        "hint": "dp[0] = 1; dp[1] = 1 if s[0] != '0' else 0; for i in 2..n: dp[i] = (one-digit ok ? dp[i-1] : 0) + "
                "(two-digit ok ? dp[i-2] : 0), mod MOD. Only two previous values are needed.",
        "tests": [
            (("226226226",), 27),
            ((_LONG,), _LONG_WAYS),
        ],
    },
]
