"""
Basic Calculator                                                              [hard]

Evaluate an expression string made of non-negative integers, "+", "-",
parentheses and spaces. A "-" can also negate the number or "(...)" right after
it: at the start, after "(", or after another operator, as in "-(2 + 3)" or
"4 - -2". Don't use eval().

Example:
    calculate("1 + 1")                  ->  2
    calculate(" 2-1 + 2 ")              ->  3
    calculate("(1+(4+5+2)-3)+(6+8)")    ->  23
    calculate("-(2 + 3) - -4")           ->  -1

Aim for:  O(n), reading the string once.
Hint:     Write evaluate(i) that reads from index i and returns (value, index after it). It keeps
          a running total and the sign of the next term. On "(" it calls itself and adds the
          result times the sign. On ")" (or the end) it returns. A number is read digit by digit.
"""


def calculate(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _random_expr(rng, depth):
    parts = []
    for k in range(rng.randint(1, 4)):
        if k:
            parts.append(rng.choice(["+", "-", " + ", " - "]))
        neg = "-" if rng.random() < 0.2 else ""
        if depth and rng.random() < 0.4:
            parts.append(neg + "(" + _random_expr(rng, depth - 1) + ")")
        else:
            parts.append(neg + str(rng.randint(0, 99)))
    return "".join(parts)


def _value(expr):
    return eval(expr.replace("--", "- -"))      # the reference may use eval, you may not


def _cases():
    import random
    rng = random.Random(224)
    out = []
    for _ in range(10):
        e = _random_expr(rng, 3)
        out.append(((e,), _value(e)))
    deep = "1" + "+(1" * 80 + ")" * 80          # 80 levels of nesting
    out.append(((deep,), 81))
    return out


USES = ["recursion.trust", "recursion.parse"]

TESTS = [
    (("1 + 1",), 2),
    ((" 2-1 + 2 ",), 3),
    (("(1+(4+5+2)-3)+(6+8)",), 23),
    (("-(2 + 3) - -4",), -1),
    (("42",), 42),
    (("-7",), -7),
    (("(((5)))",), 5),
    (("10 - (2 - (3 - 4))",), 7),
    (("2147483647",), 2147483647),
    (("-(-(-(1)))",), -1),
] + _cases()
