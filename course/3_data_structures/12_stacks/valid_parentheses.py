"""
Valid Parentheses                                                     [easy] · stack

`s` contains only the characters ()[]{}. Return True if every bracket is
closed by the same type of bracket, in the correct order.

Example:
    valid_parentheses("()[]{}")  ->  True
    valid_parentheses("([)]")    ->  False

Aim for:  O(n) time
Hint:     The most recent unclosed bracket must be closed first — last in,
          first out. That's a stack.
"""


def valid_parentheses(s: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


USES = ["stack.lifo"]

TESTS = [
    (("()",), True),
    (("()[]{}",), True),
    (("(]",), False),
    (("([)]",), False),
    (("{[]}",), True),
    (("(",), False),
    (("]",), False),
    (("",), True),
]
