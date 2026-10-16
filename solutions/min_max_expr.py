def min_max_expr(expr: str) -> int:
    def parse(i):
        """Value of the expression starting at expr[i], and the index just after it."""
        if expr[i].isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            return int(expr[i:j]), j
        pick = max if expr.startswith("max", i) else min
        i += 4                          # skip "max(" or "min("
        values = []
        while True:
            value, i = parse(i)         # trust the call for the inner expression
            values.append(value)
            if expr[i] == ")":
                return pick(values), i + 1
            i += 1                      # skip the ","

    return parse(0)[0]
