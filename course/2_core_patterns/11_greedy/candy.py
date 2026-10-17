"""
Candy                                                                         [hard]

Children stand in a line, each with a rating. Hand out candy so that:
- every child gets at least 1, and
- a child with a higher rating than a NEIGHBOUR gets more candy than that neighbour.

Return the smallest total number of candies.

Example:
    candy([1, 0, 2])     ->  5      2, 1, 2
    candy([1, 2, 2])     ->  4      1, 2, 1  (equal ratings don't need equal candy)
    candy([1, 3, 4, 5, 2])  ->  11  1, 2, 3, 4, 1

Aim for:  O(n) with two passes.
Hint:     The two neighbour rules are independent. Left to right: give each child 1 more than
          the left neighbour when its rating is higher, else 1. Right to left: make sure each
          child also beats its right neighbour when its rating is higher, taking the max of
          both requirements. Sum it up.
"""


def candy(ratings: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _relax(ratings):
    """Keep raising whoever breaks a rule until nobody does: the least fixed point."""
    c = [1] * len(ratings)
    changed = True
    while changed:
        changed = False
        for i in range(len(ratings)):
            for j in (i - 1, i + 1):
                if 0 <= j < len(ratings) and ratings[i] > ratings[j] and c[i] <= c[j]:
                    c[i] = c[j] + 1
                    changed = True
    return sum(c)


def _two_pass(ratings):
    n = len(ratings)
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)


def _cases():
    import random
    rng = random.Random(135)
    out = []
    for _ in range(10):
        ratings = [rng.randint(0, 5) for _ in range(rng.randint(1, 15))]
        out.append(((ratings,), _relax(ratings)))
    big = list(range(50_000, 0, -1)) + [rng.randint(0, 100) for _ in range(50_000)]
    out.append(((big,), _two_pass(big)))
    return out


USES = ["array.left_right_passes"]

TESTS = [
    (([1, 0, 2],), 5),
    (([1, 2, 2],), 4),
    (([1, 3, 4, 5, 2],), 11),
    (([5],), 1),
    (([3, 3, 3],), 3),
    (([5, 4, 3, 2, 1],), 15),
    (([1, 2, 87, 87, 87, 2, 1],), 13),
] + _cases()
