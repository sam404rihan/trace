def remove_invalid_parentheses(s: str) -> list[str]:
    extra_open = extra_close = 0        # exactly how many of each must be removed
    for ch in s:
        if ch == "(":
            extra_open += 1
        elif ch == ")":
            if extra_open:
                extra_open -= 1
            else:
                extra_close += 1

    opens_left = [0] * (len(s) + 1)     # opens_left[i]: "(" in s[i:], same for ")"
    closes_left = [0] * (len(s) + 1)
    for i in range(len(s) - 1, -1, -1):
        opens_left[i] = opens_left[i + 1] + (s[i] == "(")
        closes_left[i] = closes_left[i + 1] + (s[i] == ")")

    found = set()

    def build(i, kept, depth, rm_open, rm_close):
        if depth < 0 or rm_open > opens_left[i] or rm_close > closes_left[i]:
            return                      # unbalanced, or not enough left to remove
        if i == len(s):
            if depth == 0:
                found.add("".join(kept))
            return
        ch = s[i]
        if ch == "(" and rm_open:
            build(i + 1, kept, depth, rm_open - 1, rm_close)            # remove it
        elif ch == ")" and rm_close:
            build(i + 1, kept, depth, rm_open, rm_close - 1)
        kept.append(ch)                                                 # keep it
        build(i + 1, kept, depth + (ch == "(") - (ch == ")"), rm_open, rm_close)
        kept.pop()

    build(0, [], 0, extra_open, extra_close)
    return sorted(found)
