"""
Cheapest Flights Within K Stops                                               [medium]

Cities are 0..n-1. Each flight is [from, to, price]. Return the cheapest price
from src to dst using at most k stops (k + 1 flights), or -1 if impossible.

Example:
    cheapest_flights(4, [[0,1,100], [1,2,100], [2,0,100], [1,3,600], [2,3,200]], 0, 3, 1)  ->  700
        0 → 1 → 3 costs 700. 0 → 1 → 2 → 3 is cheaper (400) but needs 2 stops.

Aim for:  O(k · E): Bellman-Ford limited to k + 1 rounds.
Hint:     Plain Dijkstra breaks here, because a cheaper route with too many stops can block a valid
          one. Instead, relax every flight k + 1 times. Each round, read from a COPY of last round's
          prices, so one round never chains two flights together.
"""


def cheapest_flights(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, flights, src, dst, k):
    best = float("inf")
    stack = [(src, 0, 0)]
    while stack:
        city, cost, used = stack.pop()
        if city == dst:
            best = min(best, cost)
        if used == k + 1:
            continue
        for a, b, p in flights:
            if a == city:
                stack.append((b, cost + p, used + 1))
    return best if best != float("inf") else -1


def _cases():
    import random
    rng = random.Random(93)
    out = []
    for _ in range(10):
        n = rng.randint(2, 6)
        flights = []
        for _ in range(rng.randint(1, 10)):
            a, b = rng.sample(range(n), 2)
            flights.append([a, b, rng.randint(1, 50)])
        src, dst = rng.sample(range(n), 2)
        k = rng.randint(0, 3)
        out.append(((n, flights, src, dst, k), _brute(n, flights, src, dst, k)))
    return out


F = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
TESTS = [((4, F, 0, 3, 1), 700), ((4, F, 0, 3, 2), 400), ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), 500),
         ((3, [[0, 1, 100]], 0, 2, 5), -1)] + _cases()
