"""
Letter Combinations of a Phone Number                                         [medium]

On a phone keypad, 2 = "abc", 3 = "def", 4 = "ghi", 5 = "jkl", 6 = "mno",
7 = "pqrs", 8 = "tuv", 9 = "wxyz". Given a string of digits 2-9, return every
letter string they could spell, in keypad order (the first digit's letters
vary slowest). An empty input gives [].

Example:
    letter_combinations("23")  ->  ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]

Hint:     Backtrack over positions: for each letter of digits[i], append it and recurse on i + 1.
          (itertools.product does the same thing, but write the recursion once yourself.)
"""


def letter_combinations(digits: str) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


_KEYS = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def _ref(d):
    from itertools import product as prod
    return ["".join(p) for p in prod(*(_KEYS[x] for x in d))] if d else []


TESTS = [((d,), _ref(d)) for d in ("23", "", "2", "79", "234", "9999")]
