"""
A tiny search engine                                                          [build]

Build a class that indexes documents and answers word searches.

    idx = WordIndex()
    idx.add(1, "The quick brown fox")
    idx.add(2, "A quick blue hare")
    idx.search("quick")              ->  [1, 2]
    idx.search_all(["quick", "fox"]) ->  [1]
    idx.remove(1)
    idx.search("quick")              ->  [2]

Rules:
  - Words are runs of letters and digits, compared lowercase:
    "Fox!" and "fox" are the same word.
  - search(word) returns the sorted ids of documents containing that word.
  - search_all(words) returns the sorted ids containing every word.
    An empty list of words matches nothing: [].
  - add() with an id that already exists replaces that document.
  - remove(id) of an unknown id does nothing.

Aim for:  searches that don't scan every document. Map word -> set of ids
          (an inverted index), and keep id -> words so remove() is cheap.
Hint:     re.findall(r"[a-z0-9]+", text.lower()) extracts the words.
          search_all is a set intersection.
"""
import re


class WordIndex:
    def __init__(self):
        raise NotImplementedError  # set up your dicts here

    def add(self, doc_id: int, text: str) -> None:
        raise NotImplementedError

    def remove(self, doc_id: int) -> None:
        raise NotImplementedError

    def search(self, word: str) -> list[int]:
        raise NotImplementedError

    def search_all(self, words: list[str]) -> list[int]:
        raise NotImplementedError


CLASS = "WordIndex"

USES = ["hash.set_lookup"]

TESTS = [
    ([("WordIndex",), ("add", 1, "The quick brown fox"), ("add", 2, "A quick blue hare"),
      ("search", "quick"), ("search_all", ["quick", "fox"]), ("remove", 1), ("search", "quick")],
     [None, None, None, [1, 2], [1], None, [2]]),
    ([("WordIndex",), ("add", 5, "Fox! fox? FOX."), ("search", "fox"), ("search", "FOX"), ("search", "dog")],
     [None, None, [5], [5], []]),
    ([("WordIndex",), ("add", 1, "red apple"), ("add", 1, "green pear"), ("search", "apple"), ("search", "pear")],
     [None, None, None, [], [1]]),
    ([("WordIndex",), ("add", 3, "a b"), ("add", 1, "b c"), ("add", 2, "c a"),
      ("search_all", ["a"]), ("search_all", ["c", "b"]), ("search_all", []), ("remove", 99), ("search", "b")],
     [None, None, None, None, [2, 3], [1], [], None, [1, 3]]),
    ([("WordIndex",), ("add", 7, "v2 release-notes v2"), ("search", "v2"), ("search", "release"), ("search_all", ["notes", "v2"])],
     [None, None, [7], [7], [7]]),
]
