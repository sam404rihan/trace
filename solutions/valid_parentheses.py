def valid_parentheses(s: str) -> bool:
    # Push openers; each closer must match the most recent opener. O(n).
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack               # leftovers mean unclosed brackets
