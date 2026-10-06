def expression_add_operators(digits: str, target: int) -> list[str]:
    found = []

    def build(i, expr, value, last):
        """digits[:i] became expr, worth value; last is its final term (for *)."""
        if i == len(digits):
            if value == target:
                found.append(expr)
            return
        for j in range(i + 1, len(digits) + 1):
            piece = digits[i:j]
            if len(piece) > 1 and piece[0] == "0":
                break                       # no numbers with a leading zero
            x = int(piece)
            if i == 0:
                build(j, piece, x, x)
                continue
            build(j, expr + "+" + piece, value + x, x)
            build(j, expr + "-" + piece, value - x, -x)
            build(j, expr + "*" + piece, value - last + last * x, last * x)     # x binds to last

    if digits:
        build(0, "", 0, 0)
    return sorted(found)
