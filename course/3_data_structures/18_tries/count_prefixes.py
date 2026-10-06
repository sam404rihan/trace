"""
Count Words With Prefix                                                     [medium]

For each string in `prefixes`, count how many words in `words` start with it.
Return the counts in the same order. (The empty prefix matches every word.)

Example:
    count_prefixes(["apple", "app", "apply", "bat"], ["app", "ba", "c"])  ->  [3, 1, 0]

Aim for:  O(total letters in words + total letters in prefixes)
Hint:     Build a trie. At each node, store how many words pass through it.
          A query walks down its prefix and reads that count (0 if it falls off).
"""


def count_prefixes(words: list[str], prefixes: list[str]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((["apple", "app", "apply", "bat", "bath"], ["app", "ba", "c", "apple"]), [3, 2, 0, 1]),
    ((["apple", "app", "apply", "bat"], ["app", "ba", "c"]), [3, 1, 0]),
    (([], ["a"]), [0]),
    ((["a", "a"], ["a", ""]), [2, 2]),
]
