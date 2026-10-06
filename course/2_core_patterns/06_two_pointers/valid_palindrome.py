"""
Valid Palindrome                                               [easy] · two pointers

A phrase is a palindrome if it reads the same forwards and backwards after
lower-casing it and dropping every character that isn't a letter or digit.

Example:
    valid_palindrome("A man, a plan, a canal: Panama")  ->  True
    valid_palindrome("race a car")                      ->  False

Aim for:  O(n) time, O(1) extra space
Hint:     One pointer at each end, walking inwards. Skip what doesn't count.
          (str.isalnum() and str.lower() will help.)
"""


def valid_palindrome(s: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (("A man, a plan, a canal: Panama",), True),
    (("race a car",), False),
    ((" ",), True),
    (("0P",), False),
    (("No 'x' in Nixon",), True),
]
