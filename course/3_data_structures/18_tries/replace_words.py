"""
Replace Words                                                               [medium]

Replace every word in `sentence` that starts with a root from `roots` by the
SHORTEST such root. Words with no matching root stay as they are.

Example:
    replace_words(["cat", "bat", "rat"], "the cattle was rattled by the battery")
        ->  "the cat was rat by the bat"

Aim for:  O(total letters)
Hint:     Put the roots in a trie. For each word, walk the trie letter by
          letter and stop at the FIRST node that ends a root.
"""


def replace_words(roots: list[str], sentence: str) -> str:
    raise NotImplementedError  # replace this line with your solution


USES = ["trie.walk"]

TESTS = [
    ((["cat", "bat", "rat"], "the cattle was rattled by the battery"), "the cat was rat by the bat"),
    ((["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"), "a a b c"),
    (([], "hello world"), "hello world"),
    ((["ca", "cat"], "cattle"), "ca"),
]
