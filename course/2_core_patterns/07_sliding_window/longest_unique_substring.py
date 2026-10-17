"""
Longest Substring Without Repeating Characters             [medium] · sliding window

Return the length of the longest substring of `s` with no repeated characters.

Example:
    longest_unique_substring("abcabcbb")  ->  3      "abc"
    longest_unique_substring("pwwkew")    ->  3      "wke"

Aim for:  O(n) time
Hint:     Keep a window [left, right] with no repeats. Grow it on the right; when
          the new character is already inside, move `left` past its last position.
"""


def longest_unique_substring(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["window.variable"]

TESTS = [
    (("abcabcbb",), 3),
    (("bbbbb",), 1),
    (("pwwkew",), 3),
    (("",), 0),
    (("dvdf",), 3),
    (("abba",), 2),
]
