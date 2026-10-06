"""
Word Break                                                                  [medium]

Return True if `s` can be split into a sequence of one or more words from
`words` (each word can be reused).

Example:
    word_break("applepenapple", ["apple", "pen"])  ->  True
    word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])  ->  False

Aim for:  O(n²) checks with a set of words. The 4th test WILL time out with
          plain recursion. It explores the same suffixes over and over.
Hint:     can[i] = "s[:i] can be built". can[0] is True (the empty string).
          can[i] is True if some j < i has can[j] True and s[j:i] in the word set.
          (Or: plain recursion on the start index + @cache.)
"""


def word_break(s: str, words: list[str]) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (("leetcode", ["leet", "code"]), True),
    (("applepenapple", ["apple", "pen"]), True),
    (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False),
    (("a" * 40 + "b", ["a", "aa", "aaa", "aaaa"]), False),
    (("", ["a"]), True),
]
