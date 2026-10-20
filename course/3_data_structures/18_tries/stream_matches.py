"""
Stream of Characters                                                          [hard]

Letters arrive one at a time. After each one, say whether the letters so far
END with one of the words: True if some word equals the last len(word) letters.

Example:
    stream_matches(["cd", "f", "kl"], "abcdefkl")
        ->  [False, False, False, True, False, True, False, True]
        "cd" ends at the 4th letter, "f" at the 6th and "kl" at the 8th.

Aim for:  well under O(len(letters) × number of words). The big test has 2,000
          words of up to 200 letters and 100,000 letters: comparing every word at
          every letter is far too slow.
Hint:     Put every word into a trie BACKWARDS. After each letter, walk the trie
          from that newest letter back through the stream: if you reach a node
          where a word ends, answer True; if the next letter isn't in the trie,
          stop.
"""


def stream_matches(words: list[str], letters: str) -> list[bool]:
    raise NotImplementedError  # replace this line with your solution


def _fast(words, letters):
    root = {}
    for w in words:
        node = root
        for ch in reversed(w):
            node = node.setdefault(ch, {})
        node["$"] = True
    out = []
    for i in range(len(letters)):
        node, j, hit = root, i, False
        while j >= 0 and letters[j] in node:
            node = node[letters[j]]
            if "$" in node:
                hit = True
                break
            j -= 1
        out.append(hit)
    return out


def _big():
    import random
    rng = random.Random(1801)
    words = ["".join(rng.choice("abcdefghij") for _ in range(rng.randint(3, 200))) for _ in range(2_000)]
    letters = "".join(rng.choice("abcdefghij") for _ in range(100_000))
    return (words, letters), _fast(words, letters)


USES = ["trie.walk"]

TESTS = [
    ((["cd", "f", "kl"], "abcdefkl"), [False, False, False, True, False, True, False, True]),
    ((["a"], "aba"), [True, False, True]),
    ((["ab", "b"], "ab"), [False, True]),
    ((["abc", "xbc"], "xbcabc"), [False, False, True, False, False, True]),
    (([], "ab"), [False, False]),
    ((["aaa"], "aaaa"), [False, False, True, True]),
    ((["x"], ""), []),
    _big(),
]
