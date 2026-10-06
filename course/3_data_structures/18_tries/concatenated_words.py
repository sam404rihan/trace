"""
Concatenated Words                                                            [hard]

`words` holds distinct non-empty lowercase strings. A concatenated word is one
made entirely of at least TWO other (shorter) words from the list, glued
together; the same word can be used more than once. Return all concatenated
words, in the order they appear in `words`.

Example:
    concatenated_words(["cat", "cats", "catsdogcats", "dog", "dogcatsdog",
                        "hippopotamuses", "rat", "ratcatdogcat"])
        ->  ["catsdogcats", "dogcatsdog", "ratcatdogcat"]
    concatenated_words(["cat", "dog", "catdog"])  ->  ["catdog"]

Aim for:  about O(total length × word length): insert the words into a trie, then a
          word-break DP per word that walks the trie instead of slicing strings.
Hint:     can[i] = word[:i] splits into list words. For each i with can[i], walk the trie from
          word[i] onwards; at every node that ends a word (at position j), set can[j]. Don't let
          the whole word count as one of its own parts: require at least two pieces, e.g. skip
          the piece that starts at 0 and ends at len(word).
"""


def concatenated_words(words: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(words):
    vocab = set(words)
    out = []
    for w in words:
        def split(s, parts):
            if not s:
                return parts >= 2
            return any(s[:k] in vocab and split(s[k:], parts + 1) for k in range(1, len(s) + 1)
                       if not (parts == 0 and k == len(s)))
        if split(w, 0):
            out.append(w)
    return out


def _fast(words):
    vocab = set(words)
    out = []
    for w in words:
        can = [True] + [False] * len(w)
        for j in range(1, len(w) + 1):
            for i in range(j):
                if can[i] and w[i:j] in vocab and not (i == 0 and j == len(w)):
                    can[j] = True
                    break
        if can[len(w)]:
            out.append(w)
    return out


def _cases():
    import random
    rng = random.Random(472)
    out = []
    for _ in range(8):
        base = list({"".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(4)})
        glued = ["".join(rng.choice(base) for _ in range(rng.randint(2, 3))) for _ in range(3)]
        words = list(dict.fromkeys(base + glued + ["".join(rng.choice("ab") for _ in range(5))]))
        rng.shuffle(words)
        out.append(((words,), _brute(words)))
    base = list({"".join(rng.choice("abcdefgh") for _ in range(rng.randint(2, 5))) for _ in range(2000)})
    glued = ["".join(rng.choice(base) for _ in range(rng.randint(2, 6))) for _ in range(3000)]
    junk = ["".join(rng.choice("abcdefgh") for _ in range(rng.randint(10, 30))) for _ in range(1000)]
    big = list(dict.fromkeys(base + glued + junk))
    rng.shuffle(big)
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    ((["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"],),
     ["catsdogcats", "dogcatsdog", "ratcatdogcat"]),
    ((["cat", "dog", "catdog"],), ["catdog"]),
    ((["a"],), []),
    ((["a", "aa", "aaa", "aaaa"],), ["aa", "aaa", "aaaa"]),
    ((["ab", "abab", "aba"],), ["abab"]),
] + _cases()
