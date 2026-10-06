"""
Stickers to Spell Word                                                        [hard]

Each sticker is a lowercase word; you have unlimited copies of every sticker.
Cut letters out of the stickers you buy and rearrange them to spell `target`.
Return the fewest stickers you need, or -1 if it can't be done.
target has at most 15 letters.

Example:
    stickers_to_spell(["with", "example", "science"], "thehat")   ->  3
        two "with" and one "example": t, h, e, h, a, t
    stickers_to_spell(["notice", "possible"], "basicbasic")       ->  -1      no sticker has a "b"

Aim for:  O(2^t · stickers · t) with a DP over subsets of target's letters (t = len(target)).
Hint:     State: a bitmask of the target positions already covered. From a state, apply one
          sticker: walk the target and cover each uncovered position whose letter the sticker
          still has (use a letter count per sticker). BFS from mask 0 (each step = one sticker)
          gives the fewest stickers for the full mask. To cut branches, only try stickers that
          contain the first uncovered letter: some sticker must cover it eventually.
"""


def stickers_to_spell(stickers: list[str], target: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(stickers, target):
    """Memoized search on the remaining letters as a sorted string."""
    from collections import Counter
    from functools import cache
    counts = [Counter(s) for s in stickers]

    @cache
    def need(rest):
        if not rest:
            return 0
        best = float("inf")
        for c in counts:
            if rest[0] not in c:
                continue
            left = Counter(rest)
            left.subtract(c)
            nxt = "".join(sorted(left.elements()))
            best = min(best, 1 + need(nxt))
        return best

    ans = need("".join(sorted(target)))
    return -1 if ans == float("inf") else ans


def _cases():
    import random
    rng = random.Random(691)
    out = []
    for _ in range(8):
        stickers = ["".join(rng.choice("abcdefg") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 5))]
        target = "".join(rng.choice("abcdefg") for _ in range(rng.randint(1, 10)))
        out.append(((stickers, target), _ref(stickers, target)))
    stickers = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(7)) for _ in range(50)]
    target = "".join(rng.choice("abcdefghijklmn") for _ in range(15))
    out.append(((stickers, target), _ref(stickers, target)))
    return out


TESTS = [
    ((["with", "example", "science"], "thehat"), 3),
    ((["notice", "possible"], "basicbasic"), -1),
    ((["a"], "aaaaa"), 5),
    ((["ab", "ba"], "abab"), 2),
    ((["these", "guess", "about", "garden", "him"], "atomher"), 3),
] + _cases()
