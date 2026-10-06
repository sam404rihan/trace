"""
Palindrome Partitioning                                                       [medium]

Split s into pieces so that every piece is a palindrome. Return every possible
way to do it. Order doesn't matter: the tests sort your answer.

Example:
    palindrome_partition("aab")  ->  [["a", "a", "b"], ["aa", "b"]]

Hint:     backtrack(start): for every end > start where s[start:end] is a palindrome, take that piece
          and recurse from end. When start == len(s), record the pieces.
"""


def palindrome_partition(s: str) -> list[list[str]]:
    raise NotImplementedError  # replace this line with your solution


FINISH = sorted


def _brute(s):
    if not s:
        return [[]]
    out = []
    for i in range(1, len(s) + 1):
        if s[:i] == s[:i][::-1]:
            out += [[s[:i]] + rest for rest in _brute(s[i:])]
    return sorted(out)


TESTS = [((s,), _brute(s)) for s in ("aab", "a", "racecar", "abba", "abc", "aaaa", "abacabad", "")]
