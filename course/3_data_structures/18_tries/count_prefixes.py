"""
Count Words With Prefix                                                     [medium]

For each string in `prefixes`, count how many words in `words` start with it.
Return the counts in the same order. (The empty prefix matches every word.)

Example:
    count_prefixes(["apple", "app", "apply", "bat"], ["app", "ba", "c"])  ->  [3, 1, 0]

Aim for:  O(total letters in words + total letters in prefixes). The last test has 20,000
          words and 20,000 prefixes: scanning every word for every prefix times out.
Hint:     Build a trie. At each node, store how many words pass through it.
          A query walks down its prefix and reads that count (0 if it falls off).
"""


def count_prefixes(words: list[str], prefixes: list[str]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(1801)
    words = ["".join(rng.choice("abcde") for _ in range(rng.randint(3, 12))) for _ in range(20_000)]
    prefixes = ["".join(rng.choice("abcde") for _ in range(rng.randint(1, 6))) for _ in range(20_000)]
    counts = {}
    for w in words:
        for i in range(len(w) + 1):
            counts[w[:i]] = counts.get(w[:i], 0) + 1
    return (words, prefixes), [counts.get(p, 0) for p in prefixes]


USES = ["trie.walk"]

TESTS = [
    ((["apple", "app", "apply", "bat", "bath"], ["app", "ba", "c", "apple"]), [3, 2, 0, 1]),
    ((["apple", "app", "apply", "bat"], ["app", "ba", "c"]), [3, 1, 0]),
    (([], ["a"]), [0]),
    ((["a", "a"], ["a", ""]), [2, 2]),
    _big(),
]
