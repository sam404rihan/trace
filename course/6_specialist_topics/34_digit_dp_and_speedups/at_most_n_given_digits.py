"""
Numbers At Most N From Given Digits                                             [hard]

digits is a sorted list of distinct digits from '1' to '9', as strings. You may write
numbers using only these digits, each as often as you like. Return how many positive
integers you can write that are <= n.

Example:
    at_most_n_given_digits(["1", "3", "5", "7"], 100)  ->  20
        4 one-digit numbers + 16 two-digit numbers
    at_most_n_given_digits(["1", "4", "9"], 1_000_000_000)  ->  29523
    at_most_n_given_digits(["7"], 8)  ->  1

Aim for:  O(len(str(n)) · len(digits)).
Hint:     Numbers with fewer digits than n are all fine: k^1 + k^2 + ... + k^(L-1) for k digits.
          For numbers with exactly L digits, walk n's digits left to right: every allowed digit
          smaller than n's digit there frees the rest (k^(remaining) each). If n's digit itself
          is allowed, continue; otherwise stop. If you get through all of n, add 1 for n itself.
"""


def at_most_n_given_digits(digits: list[str], n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(digits, n):
    s, k = str(n), len(digits)
    L = len(s)
    total = sum(k ** i for i in range(1, L))
    for i, ch in enumerate(s):
        total += sum(1 for d in digits if d < ch) * k ** (L - i - 1)
        if ch not in digits:
            return total
    return total + 1


def _brute(digits, n):
    allowed = set(digits)
    return sum(1 for x in range(1, n + 1) if set(str(x)) <= allowed)


def _cases():
    import random
    rng = random.Random(3402)
    out = []
    for _ in range(8):
        ds = sorted(rng.sample("123456789", rng.randint(1, 5)))
        n = rng.randint(1, 5000)
        out.append(((ds, n), _brute(ds, n)))
    for _ in range(4):
        ds = sorted(rng.sample("123456789", rng.randint(1, 9)))
        n = rng.randint(1, 10**18)
        out.append(((ds, n), _ref(ds, n)))
    return out


USES = ["dp.digit"]

TESTS = [((["1", "3", "5", "7"], 100), 20), ((["1", "4", "9"], 1_000_000_000), 29523), ((["7"], 8), 1), ((["7"], 7), 1),
         ((["7"], 6), 0), ((["3", "4", "8"], 4), 2), ((["1", "2"], 21), _brute(["1", "2"], 21)),
         ((list("123456789"), 10**9), _ref(list("123456789"), 10**9))] + _cases()
