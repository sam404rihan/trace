"""
Scramble String                                                               [hard]

Scramble a string like this:
- A string of length 1 stays as it is.
- Otherwise, cut it into two non-empty parts x and y at any point, and either
  keep them as x + y or swap them to y + x. Then scramble x and y the same way,
  independently.

Return True if `t` can be produced by scrambling `s`. Both have the same length.

Example:
    scramble_string("great", "rgeat")   ->  True     "gr|eat" -> "rg|eat"
    scramble_string("abcde", "caebd")   ->  False
    scramble_string("a", "a")           ->  True

Aim for:  memoized recursion, about O(n⁴) states x cuts. Plain recursion is exponential.
Hint:     can(a, b) for equal-length a, b: if they're equal, True; if their letters differ
          (compare sorted or a Counter), False. Otherwise try every cut k: either
          can(a[:k], b[:k]) and can(a[k:], b[k:]) (no swap), or can(a[:k], b[-k:]) and
          can(a[k:], b[:-k]) (swapped). Cache on (a, b) with @cache.
"""


def scramble_string(s: str, t: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _scramble(rng, s):
    if len(s) == 1:
        return s
    k = rng.randint(1, len(s) - 1)
    x, y = _scramble(rng, s[:k]), _scramble(rng, s[k:])
    return y + x if rng.random() < 0.5 else x + y


def _ref(s, t):
    from functools import cache

    @cache
    def can(a, b):
        if a == b:
            return True
        if sorted(a) != sorted(b):
            return False
        return any(can(a[:k], b[:k]) and can(a[k:], b[k:]) or can(a[:k], b[-k:]) and can(a[k:], b[:-k])
                   for k in range(1, len(a)))
    return can(s, t)


def _cases():
    import random
    rng = random.Random(87)
    out = []
    for _ in range(5):
        s = "".join(rng.choice("abcd") for _ in range(rng.randint(2, 10)))
        out.append(((s, _scramble(rng, s)), True))
    for _ in range(6):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(2, 8)))
        t = "".join(rng.sample(s, len(s)))
        out.append(((s, t), _ref(s, t)))
    s = "abcdefghijklmnopqrstuvwxyzabcd"                   # 30 letters: needs the cache
    out.append(((s, _scramble(rng, s)), True))
    out.append((("abcdefghijklmnopqrstuvwxyzabcd", "bdacfhegjlikmonprqtvsuxzwyacbd"), _ref(
        "abcdefghijklmnopqrstuvwxyzabcd", "bdacfhegjlikmonprqtvsuxzwyacbd")))
    return out


TESTS = [
    (("great", "rgeat"), True),
    (("abcde", "caebd"), False),
    (("a", "a"), True),
    (("ab", "ba"), True),
    (("abc", "bca"), True),
    (("abcd", "bdac"), False),
    (("abc", "abd"), False),
] + _cases()
