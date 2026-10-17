"""
Non-overlapping Intervals                                                     [easy]

Return the minimum number of intervals to remove so the rest don't overlap.
Intervals that only touch (like [1, 2] and [2, 3]) don't overlap.

Example:
    non_overlapping([[1, 2], [2, 3], [3, 4], [1, 3]])  ->  1
    non_overlapping([[1, 2], [1, 2], [1, 2]])          ->  2

Aim for:  O(n log n) greedy. The last test has 20,000 intervals.
Hint:     Keeping the most intervals = removing the fewest. Sort by END. Keep an interval whenever it
          starts at or after the last kept end. Everything else gets removed.
"""


def non_overlapping(intervals: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(iv):
    n, best = len(iv), 0
    for m in range(1 << n):
        kept = sorted(iv[i] for i in range(n) if m >> i & 1)
        if all(a[1] <= b[0] for a, b in zip(kept, kept[1:])):
            best = max(best, len(kept))
    return n - best


def _make(rng):
    out = []
    for _ in range(rng.randint(1, 9)):
        s = rng.randint(0, 10)
        out.append([s, s + rng.randint(1, 4)])
    return (out,)


def _cases():
    import random
    rng = random.Random(120)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


def _big():
    import random
    out = [[i, i + 2] for i in range(20_000)]     # chained overlaps: keep every other one
    random.Random(5).shuffle(out)
    return out


TEACHES = ["intervals.earliest_end"]
USES = ["intervals.overlap"]

TESTS = [(([[1, 2], [2, 3], [3, 4], [1, 3]],), 1), (([[1, 2], [1, 2], [1, 2]],), 2), (([[1, 2], [2, 3]],), 0)] + _cases() + [((_big(),), 10_000)]
