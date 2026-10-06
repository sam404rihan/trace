"""
One bracket at a time                                                       [snippet]

You're checking brackets with a stack. Process ONE character `ch` and return
the updated stack, or None if `ch` makes the string invalid.

  - Openers ( [ {  go on top of the stack.
  - A closer ) ] }  must match the opener on top. Pop it. If the stack is
    empty or the top doesn't match, return None.

Example:
    bracket_step(["(", "["], "]")  ->  ["("]
    bracket_step(["("], "]")       ->  None
    bracket_step([], "{")          ->  ["{"]

Hint:     A dict from closer to opener makes the match test one line: {")": "(", "]": "[", "}": "{"}.
"""


def bracket_step(stack: list[str], ch: str) -> list[str] | None:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((["(", "["], "]"), ["("]),
    ((["("], "]"), None),
    (([], "{"), ["{"]),
    (([], ")"), None),
    ((["{", "("], ")"), ["{"]),
    ((["["], "("), ["[", "("]),
]
