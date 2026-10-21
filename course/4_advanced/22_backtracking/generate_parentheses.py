"""
Generate Parentheses                                                        [medium]

Return every string of n pairs of balanced parentheses, in any order.

Example:
    generate_parentheses(3)  ->  ["((()))", "(()())", "(())()", "()(())", "()()()"]

Aim for:  only build valid strings, never generate-and-filter
Hint:     Track how many "(" and ")" you've used. You may add "(" while
          opened < n, and ")" only while closed < opened.
"""


def generate_parentheses(n: int) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Any order is fine, but no duplicates."""
    return sorted(got) == sorted(expected)


USES = ["brackets.balance", "bt.core"]

TESTS = [
    ((1,), ["()"]),
    ((2,), ["(())", "()()"]),
    ((3,), ["((()))", "(()())", "(())()", "()(())", "()()()"]),
]
