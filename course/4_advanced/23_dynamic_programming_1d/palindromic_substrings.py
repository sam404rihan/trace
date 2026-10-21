"""
Palindromic Substrings                                                        [easy]

Count the substrings of s that are palindromes. Substrings at different
positions count separately, even if they're the same text.

Example:
    palindromic_substrings("abc")  ->  3      "a", "b", "c"
    palindromic_substrings("aaa")  ->  6      "a" ×3, "aa" ×2, "aaa"

Aim for:  O(n²) at worst, far less on most strings. The last test has 100,000 random letters:
          checking every substring times out.
Hint:     Every palindrome has a centre: a letter, or the gap between two letters. From each of the
          2n - 1 centres, grow outwards while both ends match; every step that works is one more palindrome.
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


def _fast(s):
    count = 0
    for centre in range(2 * len(s) - 1):
        lo, hi = centre // 2, centre // 2 + centre % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            count += 1
            lo, hi = lo - 1, hi + 1
    return count


def _big():
    import random
    rng = random.Random(2302)
    s = "".join(rng.choice("ab") for _ in range(100_000))
    return (s,), _fast(s)


TEACHES = ["palin.expand"]
USES = []

TESTS = [(("abc",), 3), (("aaa",), 6), (("",), 0), (("racecar",), 10)] + _cases() + [_big()]
