"""
Autocomplete                                                                 [guided]

For each query prefix, return up to 3 dictionary words that start with it,
in alphabetical order (the 3 alphabetically smallest). Duplicate dictionary
words count once.

Example:
    autocomplete(["mouse", "mobile", "money", "monitor", "map"], ["mo", "mon", "x"])
    ->  [["mobile", "money", "monitor"], ["money", "monitor"], []]
"""


def autocomplete(words: list[str], queries: list[str]) -> list[list[str]]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import bisect
    import random
    rng = random.Random(22)
    letters = "abcdefghij"
    words = sorted({"".join(rng.choice(letters) for _ in range(rng.randint(3, 9))) for _ in range(40_000)})
    queries = ["".join(rng.choice(letters) for _ in range(rng.randint(1, 4))) for _ in range(40_000)]
    out = []
    for q in queries:
        i = bisect.bisect_left(words, q)
        out.append([w for w in words[i:i + 3] if w.startswith(q)])
    return words[::-1], queries, out


_WORDS, _QUERIES, _OUT = _big()

USES = ["bsearch.first_true"]

STEPS = [
    {
        "title": "Make it work",
        "text": "For each query, collect the words that start with it, sort them, and keep the first 3.",
        "hint": "sorted(w for w in words if w.startswith(q))[:3]",
        "tests": [
            ((["mouse", "mobile", "money", "monitor", "map"], ["mo", "mon", "x"]),
             [["mobile", "money", "monitor"], ["money", "monitor"], []]),
            ((["apple", "app", "apply", "ape"], ["ap", "app"]), [["ape", "app", "apple"], ["app", "apple", "apply"]]),
        ],
    },
    {
        "title": "Edges",
        "text": "Duplicate words appear only once in a result. A prefix can be a whole word. The empty prefix matches everything.",
        "hint": "Deduplicate first: set(words).",
        "tests": [
            ((["cat", "cat", "car"], ["ca"]), [["car", "cat"]]),
            ((["go", "gone"], ["go"]), [["go", "gone"]]),
            ((["b", "a", "d", "c"], [""]), [["a", "b", "c"]]),
            (([], ["a"]), [[]]),
        ],
    },
    {
        "title": "Don't rescan the dictionary",
        "text": "40,000 words and 40,000 queries: scanning every word for every query is 1.6 billion checks. Sort the "
                "words once. Then all words starting with a prefix sit next to each other, beginning at "
                "bisect_left(words, prefix). Take up to 3 from there, stopping at the first one that doesn't match. "
                "(A trie that stores the top 3 at each node also works.)",
        "hint": "words = sorted(set(words)); i = bisect.bisect_left(words, q); "
                "[w for w in words[i:i + 3] if w.startswith(q)]",
        "tests": [
            ((["dog", "deer", "deal"], ["de", "do", "d"]), [["deal", "deer"], ["dog"], ["deal", "deer", "dog"]]),
            ((_WORDS, _QUERIES), _OUT),
        ],
    },
]
