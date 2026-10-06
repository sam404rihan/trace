"""
Russian Doll Envelopes                                                        [hard]

envelopes[i] = [width, height]. One envelope fits inside another only when
BOTH its width and height are strictly smaller. Return the most envelopes you
can nest one inside the next. You can't rotate them.

Example:
    russian_doll([[5, 4], [6, 4], [6, 7], [2, 3]])   ->  3      [2,3] in [5,4] in [6,7]
    russian_doll([[1, 1], [1, 1], [1, 1]])           ->  1

Aim for:  O(n log n). The O(n²) DP is too slow for the big test.
Hint:     Sort by width ascending, and for equal widths by height DESCENDING. Now the answer is
          the longest strictly increasing subsequence of the heights: the descending trick stops
          two envelopes with the same width from both being picked. Use the patience-sorting
          LIS with bisect_left for O(n log n).
"""


def russian_doll(envelopes: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _quadratic(envelopes):
    env = sorted(envelopes)
    best = [1] * len(env)
    for i in range(len(env)):
        for j in range(i):
            if env[j][0] < env[i][0] and env[j][1] < env[i][1]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


def _fast(envelopes):
    import bisect
    tails = []
    for _, h in sorted(envelopes, key=lambda e: (e[0], -e[1])):
        i = bisect.bisect_left(tails, h)
        tails[i:i + 1] = [h]
    return len(tails)


def _cases():
    import random
    rng = random.Random(354)
    out = []
    for _ in range(10):
        env = [[rng.randint(1, 8), rng.randint(1, 8)] for _ in range(rng.randint(1, 12))]
        out.append(((env,), _quadratic(env)))
    big = [[rng.randint(1, 10**5), rng.randint(1, 10**5)] for _ in range(50_000)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([[5, 4], [6, 4], [6, 7], [2, 3]],), 3),
    (([[1, 1], [1, 1], [1, 1]],), 1),
    (([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]],), 4),
    (([[1, 2]],), 1),
    (([[2, 100], [3, 200], [4, 300], [5, 500], [5, 400], [5, 250], [6, 370], [6, 360], [7, 380]],), 5),
] + _cases()
