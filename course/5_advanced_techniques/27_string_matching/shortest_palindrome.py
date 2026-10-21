"""
Shortest Palindrome                                                             [hard]

Add as few characters as possible to the FRONT of s to make a palindrome, and
return that palindrome.

Example:
    shortest_palindrome("aacecaaa")  ->  "aaacecaaa"
    shortest_palindrome("abcd")      ->  "dcbabcd"

Aim for:  O(n) with the prefix function.
Hint:     The answer keeps the longest palindromic PREFIX of s, and puts the reversed remainder in
          front of it. That prefix is the longest prefix of s that is also a suffix of reverse(s):
          compute pi on s + "#" + reverse(s), and its last value is the length.
"""


def shortest_palindrome(s: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    for L in range(len(s), -1, -1):
        if s[:L] == s[:L][::-1]:
            return s[L:][::-1] + s
    return s


def _cases():
    import random
    rng = random.Random(215)
    out = [((s,), _brute(s)) for s in ("".join(rng.choice("ab") for _ in range(rng.randint(0, 15))) for _ in range(8))]
    big = "a" * 50_000 + "b" + "a" * 49_999
    out.append(((big,), "a" * 49_999 + "b" + big))     # the longest palindromic prefix is the 50,000 a's
    return out


USES = ["str.prefix_function"]

TESTS = [(("aacecaaa",), "aaacecaaa"), (("abcd",), "dcbabcd"), (("",), ""), (("a",), "a"), (("aba",), "aba")] + _cases()
