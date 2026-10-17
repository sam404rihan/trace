"""
Longest Repeating Character Replacement                                     [medium]

You may change at most k characters of s (uppercase letters) into any other
letter. Return the length of the longest substring you can make out of one
repeated letter.

Example:
    character_replacement("ABAB", 2)     ->  4
    character_replacement("AABABBA", 1)  ->  4      "AABA" → "AAAA"

Aim for:  O(n), sliding window.
Hint:     A window is fixable if (window length - count of its most common letter) <= k.
          Grow right. While the window isn't fixable, shrink from the left. (Bonus: max_count
          never needs to decrease, because a smaller one can't produce a longer answer.)
"""


def character_replacement(s: str, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            w = s[i:j + 1]
            if len(w) - max(w.count(c) for c in set(w)) <= k:
                best = max(best, len(w))
    return best


def _cases():
    import random
    rng = random.Random(49)
    out = []
    for _ in range(8):
        s = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 18)))
        k = rng.randint(0, 4)
        out.append(((s, k), _brute(s, k)))
    return out


USES = ["window.variable"]

TESTS = [(("ABAB", 2), 4), (("AABABBA", 1), 4), (("A", 0), 1), (("ABCDE", 0), 1), (("ABBB", 0), 3)] + _cases()
