"""
Sum of Two Integers                                                           [medium]

Add two integers WITHOUT using + or -. Inputs are between -1000 and 1000.

Example:
    get_sum(1, 2)    ->  3
    get_sum(-2, 3)   ->  1

Aim for:  a loop of XOR and AND.
Hint:     a ^ b adds without carrying. (a & b) << 1 is the carry. Repeat until the carry is 0.
          Python ints never overflow, so to handle negatives, work in 32 bits with
          mask = 0xFFFFFFFF, and at the end turn values above 0x7FFFFFFF back into
          negatives with ~(x ^ mask).
"""


def get_sum(a: int, b: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(47)
    return [((x, y), x + y) for x, y in ((rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(10))]


USES = ["bits.shift_mask", "bits.xor_cancel"]

TESTS = [((1, 2), 3), ((-2, 3), 1), ((0, 0), 0), ((-1000, -1000), -2000), ((1000, -1), 999), ((-7, 7), 0)] + _cases()
