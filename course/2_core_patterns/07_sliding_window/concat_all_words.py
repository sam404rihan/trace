"""
Substring with Concatenation of All Words                                     [hard]

All strings in `words` have the same length (words can repeat). Find every start
index in `s` where some ordering of ALL the words, glued together with nothing
in between, appears. Return the indices in increasing order.

Example:
    concat_all_words("barfoothefoobarman", ["foo", "bar"])  ->  [0, 9]
        "barfoo" at 0 and "foobar" at 9.
    concat_all_words("wordgoodgoodgoodbestword", ["word", "good", "best", "good"])  ->  [8]

Aim for:  O(len(s) * word length): a sliding window per starting offset.
Hint:     Let w = word length. For each offset 0..w-1, cut s into w-sized pieces from there and
          run a sliding window over the pieces with a Counter: add a piece on the right, and while
          some word is over-counted (or the piece isn't a word at all) drop pieces from the left.
          When the window holds exactly len(words) pieces, its start is an answer.
"""


def concat_all_words(s: str, words: list[str]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, words):
    from collections import Counter
    w, need = len(words[0]), Counter(words)
    total = w * len(words)
    return [i for i in range(len(s) - total + 1)
            if Counter(s[i + j:i + j + w] for j in range(0, total, w)) == need]


def _fast(s, words):
    from collections import Counter
    w, k, need = len(words[0]), len(words), Counter(words)
    found = []
    for offset in range(w):
        have, left, count = Counter(), offset, 0
        for right in range(offset, len(s) - w + 1, w):
            piece = s[right:right + w]
            if piece not in need:
                have.clear()
                left, count = right + w, 0
                continue
            have[piece] += 1
            count += 1
            while have[piece] > need[piece]:
                have[s[left:left + w]] -= 1
                left += w
                count -= 1
            if count == k:
                found.append(left)
        # each offset's answers come out increasing; merge at the end
    return sorted(found)


def _cases():
    import random
    rng = random.Random(30)
    out = []
    for _ in range(8):
        w = rng.randint(1, 3)
        pool = ["".join(rng.choice("ab") for _ in range(w)) for _ in range(3)]
        words = [rng.choice(pool) for _ in range(rng.randint(1, 4))]
        s = "".join(rng.choice(pool + ["a" * w]) for _ in range(rng.randint(0, 12)))
        out.append(((s, words), _brute(s, words)))
    # big: many short words, so recounting every window from scratch is too slow
    words = ["".join(rng.choice("xyz") for _ in range(3)) for _ in range(800)]
    s = "".join("".join(rng.sample(words, len(words))) for _ in range(12))
    out.append(((s, words), _fast(s, words)))
    return out


TESTS = [
    (("barfoothefoobarman", ["foo", "bar"]), [0, 9]),
    (("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]), []),
    (("wordgoodgoodgoodbestword", ["word", "good", "best", "good"]), [8]),
    (("barfoofoobarthefoobarman", ["bar", "foo", "the"]), [6, 9, 12]),
    (("aaaaaa", ["aa", "aa"]), [0, 1, 2]),
    (("ab", ["abc"]), []),
    (("a", ["a"]), [0]),
] + _cases()
