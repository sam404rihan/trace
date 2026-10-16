"""
Plus One                                                                        [easy]

A non-negative number is stored digit by digit, most significant first.
Add one and return the new digit list.

Example:
    plus_one([1, 2, 9])  ->  [1, 3, 0]
    plus_one([9, 9])     ->  [1, 0, 0]

Aim for:  one pass from the right. Don't convert the whole thing to an int.
Hint:     Walk from the last digit. A 9 becomes 0 and the carry moves left. Anything
          else just goes up by one, and you're done. If every digit was 9, put a 1 in front.
"""


def plus_one(digits: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(44)
    out = []
    for _ in range(6):
        n = rng.choice([rng.randint(0, 10**6), int("9" * rng.randint(1, 12)), rng.randint(10**15, 10**16)])
        out.append((([int(d) for d in str(n)],), [int(d) for d in str(n + 1)]))
    return out


TEACHES = ["math.carry"]
USES = []

TESTS = [
    (([1, 2, 3],), [1, 2, 4]),
    (([1, 2, 9],), [1, 3, 0]),
    (([9],), [1, 0]),
    (([9, 9, 9],), [1, 0, 0, 0]),
    (([0],), [1]),
] + _cases()
