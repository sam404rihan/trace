"""
Expression Add Operators                                                      [hard]

`digits` is a string of digits. Insert "+", "-" or "*" between some of them
(or nothing, to glue digits into longer numbers) so the expression equals
`target`, using normal precedence (* before + and -). Numbers can't have a
leading zero ("05" is not allowed, "0" is). Return every way, sorted.

Example:
    expression_add_operators("123", 6)    ->  ["1*2*3", "1+2+3"]
    expression_add_operators("232", 8)    ->  ["2*3+2", "2+3*2"]
    expression_add_operators("105", 5)    ->  ["1*0+5", "10-5"]
    expression_add_operators("3456237490", 9191)  ->  []

Aim for:  O(4^n) backtracking that evaluates as it goes (no eval() at the end).
Hint:     Recurse with (index, expression so far, value so far, last term). For "+x": value + x,
          last = x. For "-x": value - x, last = -x. For "*x": multiplication binds to the last
          term only, so undo it and redo it: value - last + last * x, last = last * x.
          Try every length for the next number, but stop after a leading "0".
"""


def expression_add_operators(digits: str, target: int) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(digits, target):
    import re
    from itertools import product
    out = []
    for ops in product(["", "+", "-", "*"], repeat=len(digits) - 1):
        expr = digits[0] + "".join(o + d for o, d in zip(ops, digits[1:]))
        if any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", expr)):
            continue
        if eval(expr) == target:
            out.append(expr)
    return sorted(out)


def _cases():
    import random
    rng = random.Random(282)
    out = []
    for _ in range(10):
        digits = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 6)))
        target = rng.choice([0, 1, 5, 10, 24, rng.randint(-50, 100)])
        out.append(((digits, target), _brute(digits, target)))
    return out


TESTS = [
    (("123", 6), ["1*2*3", "1+2+3"]),
    (("232", 8), ["2*3+2", "2+3*2"]),
    (("105", 5), ["1*0+5", "10-5"]),
    (("00", 0), ["0*0", "0+0", "0-0"]),
    (("3456237490", 9191), []),
    (("1", 1), ["1"]),
    (("2147483648", -2147483648), []),
] + _cases()
