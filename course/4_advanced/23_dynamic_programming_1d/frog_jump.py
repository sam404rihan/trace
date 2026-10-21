"""
Frog Jump                                                                     [hard]

Stones sit at the increasing positions in `stones`; stones[0] is always 0. A
frog starts on the first stone, and its first jump must be exactly 1 unit. If
its last jump was k units, its next jump must be k - 1, k or k + 1 units (and
always forward). It may only land on stones. Can it reach the last stone?

Example:
    frog_jump([0, 1, 3, 5, 6, 8, 12, 17])   ->  True
        jumps of 1, 2, 2, 3, 4, 5
    frog_jump([0, 1, 2, 3, 4, 8, 9, 11])    ->  False      the gap 4 → 8 is too wide

Aim for:  O(n²): for every stone, the set of jump sizes that can land on it.
Hint:     Map each stone position to a set of "last jump" sizes that reach it. Start with
          {0: {0}}. Go through the stones in order; for each size k in its set, try k - 1, k, k + 1
          (if > 0): if position + step is a stone, add step to that stone's set.
"""


def frog_jump(stones: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _search(stones):
    """Depth-first over (stone, last jump) states, remembering the ones already tried."""
    pos = set(stones)
    goal = stones[-1]
    seen, stack = set(), [(0, 0)]
    while stack:
        p, k = stack.pop()
        if p == goal:
            return True
        for step in (k - 1, k, k + 1):
            if step > 0 and p + step in pos and (p + step, step) not in seen:
                seen.add((p + step, step))
                stack.append((p + step, step))
    return False


def _cases():
    import random
    rng = random.Random(403)
    out = []
    for _ in range(10):
        stones = [0] + sorted(rng.sample(range(1, 25), rng.randint(1, 12)))
        out.append(((stones,), _search(stones)))
    # big: a long reachable path plus distractor stones, then an end that's just out of reach
    stones, p, k = {0}, 0, 0
    for _ in range(1200):
        k = max(1, k + rng.choice((-1, 0, 1, 1)))
        p += k
        stones.add(p)
    stones |= set(rng.sample(range(1, p), 1500))
    stones = sorted(stones)
    out.append(((stones,), _search(stones)))
    out.append(((stones + [stones[-1] + 2000],), False))
    return out


USES = ["hash.set_lookup", "dp.recurrence"]

TESTS = [
    (([0, 1, 3, 5, 6, 8, 12, 17],), True),
    (([0, 1, 2, 3, 4, 8, 9, 11],), False),
    (([0, 1],), True),
    (([0, 2],), False),
    (([0, 1, 3, 6, 10, 15, 16, 21],), True),
    (([0, 1, 3, 6, 7],), False),
] + _cases()
