"""
Word Ladder                                                                     [hard]

Change begin into end one letter at a time, where every intermediate word must
be in `words` (end must be in it too). Return the number of words in the
SHORTEST such sequence, counting begin and end, or 0 if it can't be done.

Example:
    word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])  ->  5
        hit → hot → dot → dog → cog

Aim for:  BFS. Comparing every pair of words is O(n² · L). Generate neighbours by pattern instead.
Hint:     Group words by wildcard patterns: "hot" belongs to "*ot", "h*t", "ho*". Two words are
          neighbours exactly when they share a pattern. BFS from begin, level by level.
"""


def word_ladder(begin: str, end: str, words: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(begin, end, words):
    pool = set(words)
    if end not in pool:
        return 0
    dist, frontier = {begin: 1}, [begin]
    while frontier:
        nxt = []
        for w in frontier:
            for v in pool:
                if v not in dist and len(v) == len(w) and sum(a != b for a, b in zip(v, w)) == 1:
                    dist[v] = dist[w] + 1
                    nxt.append(v)
        frontier = nxt
    return dist.get(end, 0)


def _cases():
    import random
    rng = random.Random(88)
    out = []
    for _ in range(8):
        L = rng.randint(2, 3)
        words = list({"".join(rng.choice("abc") for _ in range(L)) for _ in range(rng.randint(3, 15))})
        begin = "".join(rng.choice("abc") for _ in range(L))
        end = rng.choice(words)
        out.append(((begin, end, words), _brute(begin, end, words)))
    return out


USES = ["bfs.shortest", "bfs.implicit"]

TESTS = [(("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
         (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0), (("a", "c", ["a", "b", "c"]), 2),
         (("hot", "dog", ["hot", "dog"]), 0)] + _cases()
