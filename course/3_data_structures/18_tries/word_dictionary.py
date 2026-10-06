"""
Dictionary with wildcards                                                     [build]

Build the word store behind a crossword helper, backed by a trie.

    d = WordDictionary()
    d.add("bad"); d.add("dad"); d.add("mad"); d.add("bake")
    d.search("bad")       ->  True
    d.search(".ad")       ->  True        "." matches any one letter
    d.search("b..")       ->  True
    d.search("ba")        ->  False       a prefix isn't a word
    d.count_prefix("ba")  ->  2           "bad" and "bake"

Rules:
  - add(word) returns True if the word is new, False if it was already there.
  - search(pattern) is True if some added word matches exactly, with "." matching any one letter.
  - count_prefix(p) is how many distinct added words start with p (no wildcards here).

Aim for:  search follows a single path for letters and branches only on ".".
          count_prefix is O(len(p)) if each node stores how many words pass through it.
Hint:     Node = dict of children + an `end` flag + a `count`. On add, bump count on every
          node along the path, but only if the word is new.
"""


class WordDictionary:
    def __init__(self):
        raise NotImplementedError

    def add(self, word: str) -> bool:
        raise NotImplementedError

    def search(self, pattern: str) -> bool:
        raise NotImplementedError

    def count_prefix(self, prefix: str) -> int:
        raise NotImplementedError


CLASS = "WordDictionary"


def _big():
    import random
    import re
    rng = random.Random(23)
    letters = "abcdef"
    words = {"".join(rng.choice(letters) for _ in range(rng.randint(3, 8))) for _ in range(30_000)}
    calls, out, have = [("WordDictionary",)], [None], set()
    for w in sorted(words):
        calls.append(("add", w))
        out.append(w not in have)
        have.add(w)
    ordered = sorted(have)
    import bisect
    for _ in range(20_000):
        p = "".join(rng.choice(letters) for _ in range(rng.randint(1, 3)))
        calls.append(("count_prefix", p))
        i = bisect.bisect_left(ordered, p)
        j = bisect.bisect_left(ordered, p + "{")
        out.append(j - i)
    by_len = {}
    for w in have:
        by_len.setdefault(len(w), set()).add(w)
    for _ in range(300):
        n = rng.randint(3, 8)
        pat = [rng.choice(letters) for _ in range(n)]
        for i in rng.sample(range(n), rng.randint(0, 2)):
            pat[i] = "."
        pat = "".join(pat)
        calls.append(("search", pat))
        rx = re.compile(pat)
        out.append(any(rx.fullmatch(w) for w in by_len.get(n, ())))
    return calls, out


_CALLS, _OUT = _big()

TESTS = [
    ([("WordDictionary",), ("add", "bad"), ("add", "dad"), ("add", "mad"), ("add", "bake"), ("search", "bad"),
      ("search", ".ad"), ("search", "b.."), ("search", "ba"), ("count_prefix", "ba")],
     [None, True, True, True, True, True, True, True, False, 2]),
    ([("WordDictionary",), ("add", "a"), ("add", "a"), ("count_prefix", "a"), ("search", "."), ("search", ".."),
      ("count_prefix", "")],
     [None, True, False, 1, True, False, 1]),
    ([("WordDictionary",), ("search", "x"), ("count_prefix", "x"), ("add", "xyz"), ("search", "x.z"), ("search", "..."),
      ("search", "...."), ("count_prefix", "xyz"), ("count_prefix", "xyzw")],
     [None, False, 0, True, True, True, False, 1, 0]),
    (_CALLS, _OUT),
]
