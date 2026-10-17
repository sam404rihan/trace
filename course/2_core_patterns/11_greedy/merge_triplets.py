"""
Merge Triplets to Form Target Triplet                                         [medium]

You may pick any of the triplets and merge them by taking the maximum in each
position: [a, b, c] + [x, y, z] → [max(a, x), max(b, y), max(c, z)]. Can you
end up with exactly target?

Example:
    merge_triplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5])  ->  True     merge the 1st and 3rd

Aim for:  O(n).
Hint:     A triplet with ANY value above the target's in that position can never be used, because max
          only goes up. Of the triplets that are left, check that each position of the target is
          matched by at least one of them.
"""


def merge_triplets(triplets: list[list[int]], target: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(triplets, target):
    n = len(triplets)
    for m in range(1, 1 << n):
        merged = [0, 0, 0]
        for i in range(n):
            if m >> i & 1:
                merged = [max(a, b) for a, b in zip(merged, triplets[i])]
        if merged == list(target):
            return True
    return False


def _make(rng):
    return ([[rng.randint(1, 5) for _ in range(3)] for _ in range(rng.randint(1, 7))], [rng.randint(1, 5) for _ in range(3)])


def _cases():
    import random
    rng = random.Random(117)
    out = []
    for _ in range(12):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = []

TESTS = [(([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]), True), (([[3, 4, 5], [4, 5, 6]], [3, 2, 5]), False),
         (([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]), True)] + _cases()
