def eval_rpn(tokens: list[str]) -> int:
    # Numbers wait on a stack until an operator uses the top two. O(n).
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            right = stack.pop()          # popped first = the RIGHT operand
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(int(left / right))   # truncate toward zero; // would floor
        else:
            stack.append(int(token))
    return stack.pop()

    # Tidier dispatch: ops = {"+": operator.add, "-": operator.sub, ...}
