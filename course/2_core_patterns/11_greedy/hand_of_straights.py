"""
Hand of Straights                                                             [medium]

Can the cards in hand be rearranged into groups of exactly group_size
consecutive values (like 3, 4, 5)? Every card must be used.

Example:
    hand_of_straights([1, 2, 3, 6, 2, 3, 4, 7, 8], 3)  ->  True     [1,2,3] [2,3,4] [6,7,8]
    hand_of_straights([1, 2, 3, 4, 5], 4)              ->  False

Aim for:  O(n log n).
Hint:     The smallest card left MUST start a group, because nothing smaller can come before it. So repeatedly
          take the smallest remaining value v and use one each of v, v+1, …, v+size-1 from a Counter.
          If any is missing, the answer is False.
"""


def hand_of_straights(hand: list[int], group_size: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(hand, k):
    if len(hand) % k:
        return False
    cards = sorted(hand)
    while cards:
        v = cards[0]
        for x in range(v, v + k):
            if x not in cards:
                return False
            cards.remove(x)
    return True


def _make(rng):
    hand = []
    k = rng.randint(1, 4)
    for _ in range(rng.randint(1, 4)):
        s = rng.randint(1, 8)
        hand += list(range(s, s + k))
    if rng.random() < 0.4:
        hand[rng.randrange(len(hand))] += rng.choice((-1, 1, 5))
    rng.shuffle(hand)
    return (hand, k)


def _cases():
    import random
    rng = random.Random(116)
    out = []
    for _ in range(12):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), True), (([1, 2, 3, 4, 5], 4), False), (([5], 1), True), (([1, 1, 2, 2, 3, 3], 3), True),
         (([1, 2, 4, 5], 2), True)] + _cases()
