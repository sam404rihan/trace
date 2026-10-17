"""
Gas Station                                                                   [medium]

Stations stand in a circle. Station i gives gas[i] fuel, and driving on to the
next station costs cost[i]. Starting with an empty tank, from which station can
you drive all the way round? Return its index, or -1. The answer is unique if
it exists.

Example:
    gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])  ->  3

Aim for:  O(n), one pass.
Hint:     If total gas < total cost, it's impossible. Otherwise run a tank from a candidate start.
          Whenever the tank goes negative at station i, no start between the candidate and i can
          work, so make i + 1 the new candidate and reset the tank.
"""


def gas_station(gas: list[int], cost: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _starts(gas, cost):
    n, good = len(gas), []
    for s in range(n):
        tank = 0
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            good.append(s)
    return good


def _brute(gas, cost):
    n = len(gas)
    for s in range(n):
        tank, ok = 0, True
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return s
    return -1


def _make(rng):
    n = rng.randint(1, 8)
    return ([rng.randint(0, 6) for _ in range(n)], [rng.randint(0, 6) for _ in range(n)])


def _cases():
    import random
    rng = random.Random(115)
    out = []
    for _ in range(12):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["greedy.kadane"]

TESTS = [(([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3), (([2, 3, 4], [3, 4, 3]), -1), (([5], [4]), 0), (([0, 2], [1, 1]), 1)] + \
        [c for c in _cases() if len(_starts(*c[0])) <= 1]
