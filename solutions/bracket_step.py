PAIR = {")": "(", "]": "[", "}": "{"}


def bracket_step(stack: list[str], ch: str) -> list[str] | None:
    if ch not in PAIR:                  # an opener: wait for its closer
        stack.append(ch)
        return stack
    if not stack or stack[-1] != PAIR[ch]:
        return None                     # nothing to close, or the nesting crossed
    stack.pop()
    return stack
