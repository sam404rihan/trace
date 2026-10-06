"""
Palindromic Substrings                                                        [medium]

Count the substrings of s that are palindromes. Substrings at different
positions count separately, even if they're the same text.

Example:
    palindromic_substrings("abc")  ->  3      "a", "b", "c"
    palindromic_substrings("aaa")  ->  6      "a" ×3, "aa" ×2, "aaa"

Hint:     The same expand-around-centre idea as Longest Palindromic Substring: every successful
          expansion step is one more palindrome. Count them.
"""


def palindromic_substrings(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])


def _make(rng):
    return ("".join(rng.choice("abc") for _ in range(rng.randint(0, 20))),)


def _cases():
    import random
    rng = random.Random(104)
    out = []
    for _ in range(8):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(("abc",), 3), (("aaa",), 6), (("",), 0), (("racecar",), 10)] + _cases()
