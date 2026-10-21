"""
Alien Dictionary                                                                [hard]

`words` is sorted in an alien alphabet (lowercase letters, unknown order).
Return any ordering of ALL the letters that appear which is consistent with
the list. Return "" if no ordering works: a contradiction, or a word listed
before its own prefix (like "abc" before "ab").

Any valid answer is accepted. The tests check yours against every rule.

Example:
    alien_dictionary(["wrt", "wrf", "er", "ett", "rftt"])  ->  "wertf"

Aim for:  O(total letters).
Hint:     Compare each adjacent pair of words: the first position where they differ gives one rule
          a → b. Then topologically sort the letters (Kahn's algorithm). If you can't output every
          letter, there's a cycle.
"""


def alien_dictionary(words: list[str]) -> str:
    raise NotImplementedError  # replace this line with your solution


def _rules(words):
    letters = {c for w in words for c in w}
    rules = set()
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                rules.add((x, y))
                break
        else:
            if len(a) > len(b):
                return letters, None
    return letters, rules


def _possible(letters, rules):
    indeg = {c: 0 for c in letters}
    for _, b in rules:
        indeg[b] += 1
    ready = [c for c in letters if indeg[c] == 0]
    done = 0
    while ready:
        c = ready.pop()
        done += 1
        for a, b in rules:
            if a == c:
                indeg[b] -= 1
                if indeg[b] == 0:
                    ready.append(b)
    return done == len(letters)


def CHECK(got, expected, args):
    letters, rules = _rules(args[0])
    if rules is None or not _possible(letters, rules):
        return got == ""
    if not isinstance(got, str) or sorted(got) != sorted(letters):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[a] < pos[b] for a, b in rules)


def _alien_sorted(rng):
    alphabet = list("abcdef")
    rng.shuffle(alphabet)
    rank = {c: i for i, c in enumerate(alphabet)}
    words = ["".join(rng.choice(alphabet[:4]) for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(2, 8))]
    return sorted(set(words), key=lambda w: [rank[c] for c in w])


def _describe(words):
    letters, rules = _rules(words)
    return "" if rules is None or not _possible(letters, rules) else "any valid letter order"


def _cases():
    import random
    rng = random.Random(90)
    return [((w,), _describe(w)) for w in (_alien_sorted(rng) for _ in range(8))]


_FIXED = [["wrt", "wrf", "er", "ett", "rftt"], ["z", "x"], ["z", "x", "z"], ["abc", "ab"], ["a"], ["ab", "abc"],
          ["ac", "ab", "zc", "zb"]]
USES = ["graph.adjacency", "graph.topo_kahn"]

TESTS = [((w,), _describe(w)) for w in _FIXED] + _cases()
