"""
Reverse Integer                                                               [medium]

Reverse the decimal digits of a 32-bit signed integer x. If the result falls
outside the 32-bit range [-2**31, 2**31 - 1], return 0.

Example:
    reverse_integer(123)    ->  321
    reverse_integer(-120)   ->  -21
    reverse_integer(1534236469)  ->  0      9646324351 doesn't fit in 32 bits

Hint:     Peel digits with % 10 and // 10 on abs(x), build the result, put the sign back,
          and check the range at the end.
"""


def reverse_integer(x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(x):
    r = int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)
    return r if -2**31 <= r <= 2**31 - 1 else 0


USES = []

TESTS = [((x,), _ref(x)) for x in (123, -123, 120, 0, 1534236469, -2147483648, 2147483647, 1463847412, -8463847412 // 4, 7, -10)]
