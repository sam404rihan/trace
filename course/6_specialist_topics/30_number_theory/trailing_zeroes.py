"""
Factorial Trailing Zeroes                                                       [easy]

Return how many zeros n! ends with. n can be as large as 10^18, so computing n!
is out of the question.

Example:
    trailing_zeroes(5)   ->  1        120
    trailing_zeroes(25)  ->  6        25 contributes two 5s

Aim for:  O(log n).
Hint:     Every trailing zero is a factor 10 = 2 · 5, and 2s are plentiful, so count the 5s.
          n // 5 numbers contribute one 5, n // 25 contribute a second, n // 125 a third, ...
"""


def trailing_zeroes(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(n):
    c = 0
    while n:
        n //= 5
        c += n
    return c


def _fact_zeros(n):
    f = 1
    for k in range(2, n + 1):
        f *= k
    s = str(f)
    return len(s) - len(s.rstrip("0"))


TESTS = [((3,), 0), ((5,), 1), ((0,), 0), ((25,), 6), ((100,), 24), ((124,), 28), ((125,), 31)] \
    + [((n,), _fact_zeros(n)) for n in (49, 50, 51, 99, 200)] \
    + [((n,), _ref(n)) for n in (10**9, 10**18, 123_456_789_012_345)]
