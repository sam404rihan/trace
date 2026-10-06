def longest_valid_parentheses(s: str) -> int:
    stack = [-1]                # bottom: the index just before the current valid run
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)     # an unmatched ")": runs can only start after it
            else:
                best = max(best, i - stack[-1])
    return best
