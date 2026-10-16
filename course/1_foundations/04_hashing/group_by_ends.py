"""
Group by First and Last Letter                                                [easy]

Group the words that start with the same letter AND end with the same letter.
Return the groups in the order their first word appears, with each group's
words in their original order. Words are lowercase and never empty.

Example:
    group_by_ends(["tab", "toast", "bat", "tilt", "bib", "top"])
        ->  [["tab"], ["toast", "tilt"], ["bat"], ["bib"], ["top"]]

Aim for:  O(n), one pass with a dict.
Hint:     Every word in a group shares the pair (first letter, last letter), so use
          (w[0], w[-1]) as a dict key and append each word to its key's list. A dict
          keeps its keys in the order they were added, so list(groups.values()) is
          already in the right order.
"""


def group_by_ends(words: list[str]) -> list[list[str]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["hash.group_key"]
USES = []

TESTS = [
    ((["tab", "toast", "bat", "tilt", "bib", "top"],), [["tab"], ["toast", "tilt"], ["bat"], ["bib"], ["top"]]),
    ((["a", "aa", "ab", "ba", "a"],), [["a", "aa", "a"], ["ab"], ["ba"]]),
    (([],), []),
    ((["cat"],), [["cat"]]),
    ((["dog", "dig", "dug"],), [["dog", "dig", "dug"]]),
]
