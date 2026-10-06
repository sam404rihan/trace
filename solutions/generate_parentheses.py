def generate_parentheses(n: int) -> list[str]:
    # Only ever add a bracket that keeps the string valid, so nothing is wasted.
    result, path = [], []

    def explore(opened, closed):
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if opened < n:
            path.append("(")
            explore(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            explore(opened, closed + 1)
            path.pop()

    explore(0, 0)
    return result
