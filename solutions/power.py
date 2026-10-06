def power(x: int, n: int) -> int:
    # Fast exponentiation: halve n every step, so only O(log n) multiplications.
    if n == 0:
        return 1
    half = power(x, n // 2)              # computed ONCE, not twice
    if n % 2 == 0:
        return half * half
    return half * half * x


def power_iterative(x: int, n: int) -> int:
    # Same idea without recursion: walk the bits of n.
    result = 1
    while n:
        if n & 1:                        # this bit is set: include the current power
            result *= x
        x *= x                           # x, x², x⁴, x⁸, ...
        n >>= 1
    return result
