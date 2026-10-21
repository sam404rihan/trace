"""
Exact fraction calculator                                                      [build]

Floats can't add 1/3 and 1/6 exactly. Build a calculator that does exact arithmetic
on fractions, keeping every value as a reduced numerator / denominator pair.

    evaluate_fraction("1/3 + 1/6")         ->  "1/2"
    evaluate_fraction("2 * (3/4 - 1/4)")   ->  "1"
    evaluate_fraction("-5/10")             ->  "-1/2"
    evaluate_fraction("7 / (2 - 2)")       ->  "undefined"

Rules:
  - The expression has non-negative integers, + - * /, parentheses, unary minus, and spaces.
  - * and / bind tighter than + and -; operators of equal precedence go left to right.
  - "a/b" is just division, so "1/3" is 1 divided by 3.
  - Answer "p/q" in lowest terms with q > 0, or "p" when q is 1. The sign goes on p.
  - Any division by zero anywhere makes the whole answer "undefined".
  - Do the arithmetic yourself with gcd. fractions.Fraction would do it for you, and the
    point is to see how.

Hint:     Two pieces. (1) A fraction helper: add, multiply, invert, each followed by dividing
          numerator and denominator by their gcd and moving the sign to the top.
          (2) A recursive-descent parser: expr = term (('+'|'-') term)*, term = factor
          (('*'|'/') factor)*, factor = '-' factor | '(' expr ')' | number.
"""


def evaluate_fraction(expr: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _ref(expr):
    from fractions import Fraction
    toks, i = [], 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            toks.append(int(expr[i:j])); i = j
        else:
            if c != " ":
                toks.append(c)
            i += 1
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def factor():
        t = take()
        if t == "-":
            return -factor()
        if t == "(":
            v = parse()
            take()
            return v
        return Fraction(t)

    def term():
        v = factor()
        while peek() in ("*", "/"):
            op, r = take(), factor()
            if op == "*":
                v = v * r
            else:
                if r == 0:
                    raise ZeroDivisionError
                v = v / r
        return v

    def parse():
        v = term()
        while peek() in ("+", "-"):
            op, r = take(), term()
            v = v + r if op == "+" else v - r
        return v
    try:
        v = parse()
    except ZeroDivisionError:
        return "undefined"
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def _gen(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        n = str(rng.randint(0, 12))
        return ("-" + n) if rng.random() < 0.15 else n
    op = rng.choice("+-*/")
    left, right = _gen(rng, depth - 1), _gen(rng, depth - 1)
    s = f"{left} {op} {right}" if rng.random() < 0.5 else f"{left}{op}{right}"
    return f"({s})" if rng.random() < 0.5 else s


def _cases():
    import random
    rng = random.Random(3009)
    out = []
    for _ in range(30):
        e = _gen(rng, 4)
        out.append(((e,), _ref(e)))
    long_sum = " + ".join(f"1/{k * (k + 1)}" for k in range(1, 400))
    out.append(((long_sum,), _ref(long_sum)))
    return out


USES = ["recursion.trust", "recursion.parse"]

TESTS = [(("1/3 + 1/6",), "1/2"), (("2 * (3/4 - 1/4)",), "1"), (("-5/10",), "-1/2"), (("7 / (2 - 2)",), "undefined"),
         (("0",), "0"), (("1 - 2 - 3",), "-4"), (("8 / 4 / 2",), "1"), (("2 + 3 * 4",), "14"), (("-(1/2) * -(4)",), "2"),
         (("6/-4",), "-3/2"), (("(1/2 - 1/2) / (1/3)",), "0"), (("1/(1/(1/7))",), "1/7")] + _cases()
