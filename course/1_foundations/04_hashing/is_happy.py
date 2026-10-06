"""
Happy Number                                                                    [easy]

Start from n and keep replacing it with the sum of the squares of its digits.
If you reach 1, n is happy. Some numbers never reach 1 and loop forever
instead. Return True if n is happy.

Example:
    is_happy(19)  ->  True      19 → 82 → 68 → 100 → 1
    is_happy(2)   ->  False     2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → ... loops

Aim for:  stop as soon as a number repeats.
Hint:     Keep a set of numbers you've seen. Seeing one twice means you're in a loop.
          (Or treat it as a linked list and use fast and slow pointers: no set needed.)
"""


def is_happy(n: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


TESTS = [((n,), _brute(n)) for n in (19, 2, 1, 7, 4, 116, 100, 1111111, 999_999_999)] + \
        [((n,), _brute(n)) for n in range(20, 40)]
