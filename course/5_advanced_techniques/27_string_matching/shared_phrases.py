"""
Find shared phrases                                                            [build]

A plagiarism checker compares two documents by the k-word phrases they share.
Words are runs of letters and digits, compared lowercase.

Return every k-word phrase that appears in BOTH documents, as strings of words
joined by single spaces, in the order of their first appearance in doc_a, each
listed once.

    shared_phrases("The cat sat on the mat.", "A cat sat on a hat; the cat sat on it.", 3)
    ->  ["the cat sat", "cat sat on"]

Aim for:  O(total words · k) or better. The last test compares two 100,000-word documents.
Hint:     Tokenise with re.findall(r"[a-z0-9]+", text.lower()). Put every k-word window of doc_b
          into a set (tuples hash fine). Then walk doc_a's windows in order. A polynomial rolling
          hash over word ids gets each step down to O(1).
"""


def shared_phrases(doc_a: str, doc_b: str, k: int) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _ref(a, b, k):
    import re as _re
    wa, wb = _re.findall(r"[a-z0-9]+", a.lower()), _re.findall(r"[a-z0-9]+", b.lower())
    in_b = {tuple(wb[i:i + k]) for i in range(len(wb) - k + 1)}
    out, seen = [], set()
    for i in range(len(wa) - k + 1):
        t = tuple(wa[i:i + k])
        if t in in_b and t not in seen:
            seen.add(t)
            out.append(" ".join(t))
    return out


def _docs(rng, n, vocab):
    words = [rng.choice(vocab) for _ in range(n)]
    return " ".join(w if rng.random() > 0.1 else w.capitalize() + rng.choice(",.;!") for w in words)


def _cases():
    import random
    rng = random.Random(218)
    vocab = ["the", "a", "data", "model", "graph", "tree", "cat", "sat", "on", "run", "fast", "slow", "x1", "is"]
    out = []
    for _ in range(4):
        a, b = _docs(rng, rng.randint(5, 40), vocab), _docs(rng, rng.randint(5, 40), vocab)
        k = rng.randint(1, 4)
        out.append(((a, b, k), _ref(a, b, k)))
    big_vocab = [f"w{i}" for i in range(3000)]
    a, b = _docs(rng, 100_000, big_vocab), _docs(rng, 100_000, big_vocab)
    out.append(((a, b, 2), _ref(a, b, 2)))
    return out


TESTS = [(("The cat sat on the mat.", "A cat sat on a hat; the cat sat on it.", 3), ["the cat sat", "cat sat on"]),
         (("one two", "one two", 3), []), (("Hello, WORLD!", "hello world", 2), ["hello world"]),
         (("a b a b a", "b a b", 2), ["a b", "b a"])] + _cases()
