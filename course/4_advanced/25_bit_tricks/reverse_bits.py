"""
Reverse the bits                                                             [guided]

Treat x as exactly `width` bits (padding with leading zeros) and reverse
their order: bit 0 swaps with bit width − 1, bit 1 with bit width − 2, and so on.

Example:
    reverse_bits(0b0001, 4)  ->  0b1000  (8)
    reverse_bits(0b0110, 4)  ->  0b0110  (6)

Use shifts and masks, not string formatting.
"""


def reverse_bits(x: int, width: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["bits.shift_mask"]

STEPS = [
    {
        "title": "Peel and push",
        "text": "Repeat `width` times: take the lowest bit of x (x & 1), shift your result left to make room and add "
                "that bit (result = (result << 1) | bit), then shift x right (x >>= 1).",
        "hint": "The first bit you peel off becomes the highest bit of the result, because it gets shifted left width - 1 more times.",
        "tests": [
            ((0b0001, 4), 0b1000),
            ((0b0110, 4), 0b0110),
            ((0b1011, 4), 0b1101),
        ],
    },
    {
        "title": "Leading zeros matter",
        "text": "The width counts too: 1 reversed as 8 bits is 0b10000000 = 128, not 1. Zero stays zero.",
        "hint": "Loop exactly `width` times, even when x has become 0.",
        "tests": [
            ((1, 8), 128),
            ((0, 8), 0),
            ((0b00010011, 8), 0b11001000),
            ((1, 1), 1),
        ],
    },
    {
        "title": "32 bits",
        "text": "Same idea at the classic size. Check that your loop handles big values and high bits.",
        "hint": "Python ints don't overflow, so nothing changes. The loop just runs 32 times.",
        "tests": [
            ((43261596, 32), 964176192),
            ((4294967293, 32), 3221225471),
            ((2 ** 31, 32), 1),
        ],
    },
]
