"""
Sum of All Pair Distances                                                     [hard]

Houses stand on a straight road at positions `xs` (any order, repeats allowed).
Return the sum of |xs[i] - xs[j]| over every pair i < j.

There can be 100,000 houses. Looping over all pairs is too slow.

Example:
    sum_pair_distances([1, 3, 6])     ->  10       2 + 5 + 3
    sum_pair_distances([4, 4, 4])     ->  0
    sum_pair_distances([5, 1])        ->  4

Aim for:  O(n log n): sort, then one pass.
Hint:     After sorting, xs[k] is the larger end of its pair with each of the k houses before it.
          Its share of the total is k * xs[k] - (sum of those k houses). Keep that sum as you go.
"""


def sum_pair_distances(xs: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(xs):
    return sum(abs(xs[i] - xs[j]) for i in range(len(xs)) for j in range(i + 1, len(xs)))


def _fast(xs):
    total, before = 0, 0
    for k, x in enumerate(sorted(xs)):
        total += k * x - before
        before += x
    return total


def _cases():
    import random
    rng = random.Random(77)
    out = []
    for _ in range(6):
        xs = [rng.randint(-50, 50) for _ in range(rng.randint(0, 25))]
        out.append(((xs,), _brute(xs)))
    big = [rng.randint(0, 10**9) for _ in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


USES = []

TESTS = [
    (([1, 3, 6],), 10),
    (([4, 4, 4],), 0),
    (([5, 1],), 4),
    (([],), 0),
    (([-3, 3],), 6),
    (([10, 0, 5, 5],), 30),
] + _cases()
