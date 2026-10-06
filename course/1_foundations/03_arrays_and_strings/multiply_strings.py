"""
Multiply Strings                                                              [medium]

Multiply two non-negative integers given as decimal strings, and return the
product as a string. Do it the way you would on paper: no converting the
whole inputs to int.

Example:
    multiply_strings("123", "456")  ->  "56088"
    multiply_strings("0", "52")     ->  "0"

Aim for:  O(len(a) · len(b)), like long multiplication.
Hint:     The product has at most len(a) + len(b) digits. Digit a[i] times digit b[j] adds to
          position i + j + 1 of the result array (counting from the left). Then sweep right
          to left, carrying.
"""


def multiply_strings(a: str, b: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(45)
    out = []
    for _ in range(8):
        x, y = rng.randint(0, 10 ** rng.randint(1, 30)), rng.randint(0, 10 ** rng.randint(1, 30))
        out.append(((str(x), str(y)), str(x * y)))
    return out


TESTS = [
    (("2", "3"), "6"),
    (("123", "456"), "56088"),
    (("0", "52"), "0"),
    (("999", "999"), "998001"),
    (("1", "1"), "1"),
] + _cases()
