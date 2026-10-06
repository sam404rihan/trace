"""
Combination Sum II                                                            [medium]

Find every unique combination of numbers from `candidates` that adds up to
target. Each candidate can be used at most once, and candidates may contain
duplicates, but no combination may appear twice. Return each combination in
increasing order, and the list of combinations sorted.

Example:
    combination_sum_ii([10, 1, 2, 7, 6, 1, 5], 8)  ->  [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

Aim for:  backtracking with two prunes.
Hint:     Sort first. In the loop at each level, skip a candidate equal to the previous one at the
          SAME level (i > start and c[i] == c[i-1]): that removes duplicate combinations. Also stop
          the loop once c[i] > what's still needed.
"""


def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _brute(c, t):
    from itertools import combinations as comb
    found = set()
    for r in range(1, len(c) + 1):
        for pick in comb(c, r):
            if sum(pick) == t:
                found.add(tuple(sorted(pick)))
    return [list(x) for x in sorted(found)]


def _cases():
    import random
    rng = random.Random(81)
    out = []
    for _ in range(8):
        c = [rng.randint(1, 8) for _ in range(rng.randint(1, 11))]
        t = rng.randint(1, 15)
        out.append(((c, t), _brute(c, t)))
    return out


TESTS = [(([10, 1, 2, 7, 6, 1, 5], 8), [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]), (([2, 5, 2, 1, 2], 5), [[1, 2, 2], [5]]),
         (([1], 2), []), (([1, 1, 1, 1], 2), [[1, 1]])] + _cases()
