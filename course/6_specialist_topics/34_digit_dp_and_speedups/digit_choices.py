"""
Digit choices under a limit                                                  [snippet]

Digit DP builds numbers no bigger than N one digit at a time. digits holds N's digits,
i is the position being filled, and tight says whether every earlier digit matched N's
exactly. Return every legal digit for position i, each paired with the tight flag for
the next position: [(digit, next_tight), ...] in increasing digit order.

Example:
    digit_choices([3, 5, 2], 1, True)   ->  [(0, False), (1, False), ..., (4, False), (5, True)]
    digit_choices([3, 5, 2], 1, False)  ->  [(0, False), (1, False), ..., (9, False)]

Hint:     top = digits[i] if tight else 9
          return [(d, tight and d == top) for d in range(top + 1)]
"""


def digit_choices(digits: list[int], i: int, tight: bool) -> list[tuple[int, bool]]:
    raise NotImplementedError  # replace this line with your solution


def FINISH(value):
    return [tuple(x) for x in value] if isinstance(value, list) else value


def _ref(digits, i, tight):
    top = digits[i] if tight else 9
    return [(d, tight and d == top) for d in range(top + 1)]


def _cases():
    import random
    rng = random.Random(3401)
    out = []
    for _ in range(8):
        digits = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(rng.randint(0, 6))]
        i, tight = rng.randrange(len(digits)), rng.random() < 0.6
        out.append(((digits, i, tight), _ref(digits, i, tight)))
    return out


TEACHES = ["dp.digit"]
USES = []

TESTS = [(([3, 5, 2], 1, True), _ref([3, 5, 2], 1, True)), (([3, 5, 2], 1, False), _ref([3, 5, 2], 1, False)),
         (([1, 0, 0], 2, True), [(0, True)]), (([9], 0, True), _ref([9], 0, True))] + _cases()
