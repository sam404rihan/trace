"""
Valid Anagram                                              [easy] · arrays and hashing

Return True if `t` is an anagram of `s`: the same letters, each used the same
number of times, just rearranged.

Example:
    valid_anagram("anagram", "nagaram")  ->  True
    valid_anagram("rat", "car")          ->  False

Aim for:  O(n) time
Hint:     Sorting both strings works in O(n log n). Can you count letters instead?
"""


def valid_anagram(s: str, t: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    (("anagram", "nagaram"), True),
    (("rat", "car"), False),
    (("a", "ab"), False),
    (("", ""), True),
    (("aacc", "ccac"), False),
]
