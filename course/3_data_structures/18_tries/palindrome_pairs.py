"""
Palindrome Pairs                                                              [hard]

`words` holds distinct strings (one of them may be ""). Return every pair of
indices [i, j] with i != j such that words[i] + words[j] is a palindrome,
sorted.

Example:
    palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"])
        ->  [[0, 1], [1, 0], [2, 4], [3, 2]]
        "abcddcba", "dcbaabcd", "llssssll", "slls"
    palindrome_pairs(["a", ""])  ->  [[0, 1], [1, 0]]

Aim for:  O(total length × word length). Checking all pairs is O(n² × length): too slow for
          the big test.
Hint:     For each word w, split it at every point into prefix + suffix.
          - If prefix is a palindrome and reversed(suffix) is another word u, then u + w works.
          - If suffix is a palindrome and reversed(prefix) is another word u, then w + u works.
          A dict from word to index answers "is reversed(...) a word?" in O(length). (A trie of
          the reversed words does the same job.) Watch out for counting the same pair twice
          when the cut is at either end: collect pairs in a set.
"""


def palindrome_pairs(words: list[str]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _brute(words):
    return [[i, j] for i in range(len(words)) for j in range(len(words))
            if i != j and words[i] + words[j] == (words[i] + words[j])[::-1]]


def _fast(words):
    index = {w: i for i, w in enumerate(words)}
    found = set()
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            pre, suf = w[:cut], w[cut:]
            if pre == pre[::-1] and suf[::-1] in index and index[suf[::-1]] != i:
                found.add((index[suf[::-1]], i))
            if suf == suf[::-1] and pre[::-1] in index and index[pre[::-1]] != i:
                found.add((i, index[pre[::-1]]))
    return [list(p) for p in sorted(found)]


def _cases():
    import random
    rng = random.Random(336)
    out = []
    for _ in range(8):
        words = list({"".join(rng.choice("ab") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(1, 9))})
        out.append(((words,), _brute(words)))
    big = list({"".join(rng.choice("abc") for _ in range(rng.randint(1, 10))) for _ in range(5000)})
    out.append(((big,), _fast(big)))
    return out


USES = ["hash.complement"]

TESTS = [
    ((["abcd", "dcba", "lls", "s", "sssll"],), [[0, 1], [1, 0], [2, 4], [3, 2]]),
    ((["bat", "tab", "cat"],), [[0, 1], [1, 0]]),
    ((["a", ""],), [[0, 1], [1, 0]]),
    ((["abc"],), []),
    ((["a", "aa", "aaa"],), [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]]),
] + _cases()
