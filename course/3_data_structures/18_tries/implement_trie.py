"""
Implement Trie (Prefix Tree)                                                  [medium]

Build the classic trie:

    insert(word)          store a word
    search(word)          True if exactly this word was inserted
    starts_with(prefix)   True if any inserted word starts with prefix

Example:
    t = Trie()
    t.insert("apple")
    t.search("apple")     ->  True
    t.search("app")       ->  False
    t.starts_with("app")  ->  True
    t.insert("app")
    t.search("app")       ->  True

Aim for:  O(length of the word) for every operation.
Hint:     Each node is a dict of children plus an `end` flag. Write one helper that walks a string
          down the trie and returns the last node (or None), and both queries become one-liners.
"""


class Trie:
    def __init__(self):
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError


CLASS = "Trie"


def _cases():
    import random
    rng = random.Random(75)
    out = []
    for size in (60, 6000):
        ops, words, res = [("Trie",)], set(), [None]
        for _ in range(size):
            w = "".join(rng.choice("abc") for _ in range(rng.randint(1, 6)))
            r = rng.random()
            if r < 0.4:
                ops.append(("insert", w)); words.add(w); res.append(None)
            elif r < 0.7:
                ops.append(("search", w)); res.append(w in words)
            else:
                ops.append(("starts_with", w)); res.append(any(x.startswith(w) for x in words))
        out.append((ops, res))
    return out


USES = ["trie.walk"]

TESTS = [([("Trie",), ("insert", "apple"), ("search", "apple"), ("search", "app"), ("starts_with", "app"),
           ("insert", "app"), ("search", "app")],
          [None, None, True, False, True, None, True]),
         ([("Trie",), ("search", "a"), ("starts_with", ""), ("insert", ""), ("search", "")],
          [None, False, False, None, True])] + _cases()
