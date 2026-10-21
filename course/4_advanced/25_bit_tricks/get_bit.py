"""
Read one bit                                                                [snippet]

Return bit k of x (0 or 1). Bit 0 is the lowest (rightmost) bit.

Example:
    get_bit(0b1010, 1)  ->  1
    get_bit(0b1010, 2)  ->  0

Hint:     Slide bit k down to position 0 with x >> k, then keep only that bit with & 1.
"""


def get_bit(x: int, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bits.shift_mask"]
USES = []

TESTS = [
    ((0b1010, 1), 1),
    ((0b1010, 2), 0),
    ((1, 0), 1),
    ((0, 5), 0),
    ((2 ** 40, 40), 1),
    ((255, 8), 0),
]
