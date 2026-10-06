def calculate(s: str) -> int:
    s = s.replace(" ", "")

    def evaluate(i):
        """Value of the expression starting at s[i], up to the matching ')' or the end."""
        total, sign = 0, 1
        while i < len(s):
            ch = s[i]
            if ch.isdigit():
                num = 0
                while i < len(s) and s[i].isdigit():
                    num = num * 10 + int(s[i])
                    i += 1
                total += sign * num
                sign = 1
                continue
            if ch == "+":
                pass                            # sign is already +1 after a term
            elif ch == "-":
                sign = -sign                    # binary minus, or a negation: both flip the sign
            elif ch == "(":
                inner, i = evaluate(i + 1)      # returns the index just past its ')'
                total += sign * inner
                sign = 1
                continue
            elif ch == ")":
                return total, i + 1
            i += 1
        return total, i

    return evaluate(0)[0]
