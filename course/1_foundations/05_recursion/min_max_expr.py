"""
Nested Min and Max                                                            [easy]

`expr` is either a whole number, or max(...) or min(...) around a list of
expressions separated by commas, nested as deep as you like. There are no
spaces. Return its value.

Example:
    min_max_expr("max(1,min(4,2),3)")       ->  3       min(4,2) is 2, then max(1,2,3) is 3
    min_max_expr("min(max(1,9),max(4,5))")  ->  5
    min_max_expr("7")                       ->  7

Aim for:  O(len(expr)): read each character once.
Hint:     Write parse(i): it reads the expression that starts at expr[i] and returns
          (its value, the index just after it). A digit: read the whole number. "max(" or
          "min(": skip those 4 characters, then call parse for each argument, stepping over
          the "," between them. At the ")", return the max or min and the index after it.
"""


def min_max_expr(expr: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["recursion.parse"]
USES = ["recursion.trust"]

TESTS = [
    (("max(1,min(4,2),3)",), 3),
    (("7",), 7),
    (("min(max(1,9),max(4,5))",), 5),
    (("max(10,2)",), 10),
    (("min(3)",), 3),
    (("max(min(5,max(6,7)),4,min(9,8))",), 8),
    (("min(max(0,0),12,max(min(30,40),25))",), 0),
    (("max(" * 50 + "1" + ")" * 50,), 1),
]
