"""
Repeated Substring Pattern                                                      [easy]

Return True if s is some shorter string repeated two or more times.

Example:
    repeated_substring_pattern("abab")          ->  True     "ab" twice
    repeated_substring_pattern("aba")           ->  False
    repeated_substring_pattern("abcabcabcabc")  ->  True

Hint:     Neat trick: s repeats exactly when s appears inside (s + s) with the first and last
          characters removed. With the prefix function: let p = n - pi[-1]. The answer is
          pi[-1] > 0 and n % p == 0.
"""


def repeated_substring_pattern(s: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    n = len(s)
    return any(n % L == 0 and s[:L] * (n // L) == s for L in range(1, n // 2 + 1))


def _cases():
    import random
    rng = random.Random(217)
    out = []
    for _ in range(10):
        if rng.random() < 0.5:
            unit = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
            s = unit * rng.randint(1, 4)
        else:
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
        out.append(((s,), _brute(s)))
    return out


USES = ["str.prefix_function"]

TESTS = [(("abab",), True), (("aba",), False), (("abcabcabcabc",), True), (("a",), False), (("aaaa",), True)] + _cases()
