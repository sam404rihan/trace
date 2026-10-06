"""
Find every occurrence                                                        [guided]

Return the start index of every occurrence of pattern in text, in increasing
order. Occurrences may overlap. pattern is never empty.

Example:
    find_all("abababa", "aba")  ->  [0, 2, 4]
    find_all("hello", "xyz")    ->  []

Write the matching yourself: no str.find, `in`, or regular expressions.
"""


def find_all(text: str, pattern: str) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


def _big():
    # Near-misses everywhere: every window starts with thousands of matching a's before failing.
    text = ("a" * 14_999 + "b") * 20
    pattern = "a" * 15_000 + "b"
    return text, pattern


def _rand(seed, count):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 25)))
        p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        out.append(((t, p), _brute(t, p)))
    return out


_BT, _BP = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Try every start position i and compare text[i:i+m] with the pattern. That's O(n · m), fine for now.",
        "hint": "for i in range(len(text) - len(pattern) + 1): compare character by character (or with a slice).",
        "tests": [(("abababa", "aba"), [0, 2, 4]), (("hello", "ll"), [2])] + _rand(212, 4),
    },
    {
        "title": "Edges",
        "text": "Overlapping matches, a pattern longer than the text, a match at the very end, an empty text.",
        "hint": "Make sure the loop's upper bound lets a match finish exactly at the last character.",
        "tests": [(("aaaa", "aa"), [0, 1, 2]), (("ab", "abc"), []), (("xyzab", "ab"), [3]), (("", "a"), [])] + _rand(213, 4),
    },
    {
        "title": "Make it fast: KMP",
        "text": "The last text is 300,000 characters and the pattern 15,001: every start position almost matches, so the "
                "naive comparison costs billions of steps. KMP never moves backwards in the text. On a mismatch, it falls back "
                "to the longest border of what it already matched (the prefix function).",
        "hint": "Compute pi for the pattern. Walk the text with k = matched length: while k and text[i] != pattern[k]: "
                "k = pi[k - 1]. If they're equal, k += 1. If k == m: record i - m + 1 and set k = pi[k - 1].",
        "tests": [(("abcabcab", "cab"), [2, 5]), ((_BT, _BP), [])],      # no run of 15,000 a's exists
    },
]
