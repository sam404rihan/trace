"""
Cheapest Team for All Skills                                                  [easy]

There are k skills, numbered 0 to k - 1 (k is at most 12). Person i knows the
skills in people[i] and costs costs[i] to hire. Return the smallest total cost
of a team that, between them, knows every skill, or -1 if no team does.

Example:
    cheapest_team([[0], [1, 2], [0, 1], [2]], [4, 5, 3, 1], 3)  ->  4
        person 2 knows 0 and 1, person 3 knows 2: 3 + 1.

Aim for:  O(2^k * people). Trying every team is O(2^people), and the last test
          has 60 people.
Hint:     Write a set of skills as a bitmask: skill s is bit 1 << s. best[mask] = cheapest
          team that knows at least the skills in mask, starting with best[0] = 0. Go through
          the masks in increasing order, and for each person p, best[mask | p_mask] can be
          best[mask] + costs[p].
"""


def cheapest_team(people: list[list[int]], costs: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(people, costs, k):
    full, inf = (1 << k) - 1, float("inf")
    masks = [sum(1 << s for s in skills) for skills in people]
    best = [inf] * (1 << k)
    best[0] = 0
    for mask in range(1 << k):
        if best[mask] < inf:
            for m, c in zip(masks, costs):
                if best[mask] + c < best[mask | m]:
                    best[mask | m] = best[mask] + c
    return best[full] if best[full] < inf else -1


def _big():
    import random
    rng = random.Random(2501)
    people = [rng.sample(range(12), rng.randint(1, 3)) for _ in range(60)]
    costs = [rng.randint(1, 1000) for _ in range(60)]
    return (people, costs, 12), _fast(people, costs, 12)


TEACHES = ["dp.bitmask"]
USES = ["bits.shift_mask"]

TESTS = [
    (([[0], [1, 2], [0, 1], [2]], [4, 5, 3, 1], 3), 4),
    (([[0, 1, 2]], [7], 3), 7),
    (([[0], [1]], [1, 1], 3), -1),
    (([[0], [0], [1]], [5, 2, 3], 2), 5),
    (([[0, 1], [1, 2], [2, 3], [0, 3]], [3, 3, 3, 3], 4), 6),
    (([], [], 1), -1),
    _big(),
]
