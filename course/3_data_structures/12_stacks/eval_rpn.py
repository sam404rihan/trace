"""
Evaluate Reverse Polish Notation                                            [medium]

Evaluate an expression written in Reverse Polish Notation: each operator
comes AFTER its two operands. Tokens are integers or one of + - * /.
Division truncates toward zero (so -7 / 2 is -3).

Example:
    eval_rpn(["2", "1", "+", "3", "*"])  ->  9      (2 + 1) * 3

Aim for:  O(n)
Hint:     Push numbers onto a stack. On an operator, pop two (careful: the
          first pop is the RIGHT operand), apply it, push the result.
          Python's // floors (-7 // 2 == -4). Use int(a / b) instead.
"""


def eval_rpn(tokens: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["stack.lifo"]

TESTS = [
    ((["2", "1", "+", "3", "*"],), 9),
    ((["4", "13", "5", "/", "+"],), 6),
    ((["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), 22),
    ((["7"],), 7),
    ((["7", "-2", "/"],), -3),
]
