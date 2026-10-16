"""
Reverse Words                                                                 [easy]

Return the words of `s` in reverse order, separated by single spaces.
`s` may have extra spaces at the start, end, or between words.

Example:
    reverse_words("the sky is blue")    ->  "blue is sky the"
    reverse_words("  hello   world  ")  ->  "world hello"

Aim for:  O(n). This is a one-liner with the right built-ins.
Hint:     s.split() with no argument splits on any run of spaces and drops
          empty pieces. Then reversed() and " ".join().
"""


def reverse_words(s: str) -> str:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (("the sky is blue",), "blue is sky the"),
    (("  hello   world  ",), "world hello"),
    (("a good   example",), "example good a"),
    (("one",), "one"),
]
