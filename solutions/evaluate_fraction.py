def _make(p, q):
    if q < 0:
        p, q = -p, -q
    g = gcd(p, q) or 1
    return p // g, q // g


def evaluate_fraction(expr: str) -> str:
    toks, i = [], 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            toks.append(int(expr[i:j]))
            i = j
        else:
            if not c.isspace():
                toks.append(c)
            i += 1
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]

    def factor():
        t = take()
        if t == "-":
            p, q = factor()
            return -p, q
        if t == "(":
            v = expr_()
            take()                                  # the ")"
            return v
        return t, 1

    def term():
        a, b = factor()
        while peek() in ("*", "/"):
            op = take()
            c, d = factor()
            if op == "*":
                a, b = _make(a * c, b * d)
            else:
                if c == 0:
                    raise ZeroDivisionError
                a, b = _make(a * d, b * c)
        return a, b

    def expr_():
        a, b = term()
        while peek() in ("+", "-"):
            op = take()
            c, d = term()
            a, b = _make(a * d + (c if op == "+" else -c) * b, b * d)
        return a, b

    try:
        p, q = expr_()
    except ZeroDivisionError:
        return "undefined"
    return str(p) if q == 1 else f"{p}/{q}"
