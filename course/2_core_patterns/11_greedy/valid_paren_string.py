"""
Valid Parenthesis String                                                      [medium]

s contains "(", ")" and "*", where each "*" can be "(", ")" or nothing.
Return True if some choice of the stars makes s a valid bracket string.

Example:
    valid_paren_string("(*)")   ->  True
    valid_paren_string("(*))")  ->  True
    valid_paren_string(")(")    ->  False

Aim for:  O(n) time, O(1) space.
Hint:     Track the RANGE of possible open-bracket counts [low, high]. "(" raises both. ")" lowers both.
          "*" lowers low and raises high. If high < 0, fail. Clamp low at 0. Valid if low == 0 at the end.
"""


def valid_paren_string(s: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    from itertools import product as prod
    stars = [i for i, ch in enumerate(s) if ch == "*"]
    for choice in prod("()", repeat=len(stars)) if stars else [()]:
        for drop in range(1 << len(stars)):
            chars = list(s)
            for k, i in enumerate(stars):
                chars[i] = "" if drop >> k & 1 else choice[k]
            bal = 0
            for ch in chars:
                bal += 1 if ch == "(" else -1 if ch == ")" else 0
                if bal < 0:
                    break
            else:
                if bal == 0:
                    return True
    return False


def _make(rng):
    return ("".join(rng.choice("()*") for _ in range(rng.randint(0, 6))),)


def _cases():
    import random
    rng = random.Random(119)
    out = []
    for _ in range(14):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["brackets.balance"]

TESTS = [(("(*)",), True), (("(*))",), True), ((")(",), False), (("",), True), (("((*",), False), (("*)",), True)] + _cases()
