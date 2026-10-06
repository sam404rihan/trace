"""
Group Anagrams                                           [medium] · arrays and hashing

Group the words that are anagrams of each other. Return a list of groups;
the groups, and the words inside each group, can be in any order.

Example:
    group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        ->  [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

Aim for:  O(n · k log k) time, where k is the length of the longest word
Hint:     Anagrams share something you can compute from each word.
          Use it as a dictionary key.
"""


def group_anagrams(words: list[str]) -> list[list[str]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Groups, and the words inside them, may come back in any order."""
    def normalize(groups):
        return sorted(sorted(group) for group in groups)
    return normalize(got) == normalize(expected)


TESTS = [
    ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
    (([""],), [[""]]),
    ((["a"],), [["a"]]),
    ((["abc", "bca", "xyz", "cab", "zyx", "q"],), [["abc", "bca", "cab"], ["xyz", "zyx"], ["q"]]),
]
