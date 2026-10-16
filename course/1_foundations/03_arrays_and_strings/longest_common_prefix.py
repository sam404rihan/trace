"""
Longest Common Prefix                                                         [easy]

Return the longest string that every word in `words` starts with.
Return "" if there isn't one.

Example:
    longest_common_prefix(["flower", "flow", "flight"])  ->  "fl"
    longest_common_prefix(["dog", "racecar", "car"])     ->  ""

Aim for:  O(total characters)
Hint:     zip(*words) gives you the words column by column, and it stops at
          the shortest word. Keep going while every letter in a column matches.
"""


def longest_common_prefix(words: list[str]) -> str:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    ((["flower", "flow", "flight"],), "fl"),
    ((["dog", "racecar", "car"],), ""),
    ((["a"],), "a"),
    ((["ab", "abc", "abcd"],), "ab"),
    ((["", ""],), ""),
]
