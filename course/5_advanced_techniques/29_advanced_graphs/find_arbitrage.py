"""
Currency arbitrage finder                                                      [build]

Exchange rates are [from, to, rate]: 1 unit of `from` buys `rate` units of `to`.
Arbitrage is a cycle of trades that ends with MORE money than you started with:
the product of the rates around the cycle is greater than 1.

Return one profitable cycle as a list of currencies whose first and last elements
are the same (like ["USD", "EUR", "GBP", "USD"]), or [] if no cycle is profitable.

    find_arbitrage([["USD", "EUR", 0.9], ["EUR", "GBP", 0.9], ["GBP", "USD", 1.3]])
    ->  ["USD", "EUR", "GBP", "USD"]        0.9 · 0.9 · 1.3 = 1.053

Rules:
  - Any profitable cycle is accepted. The tests check that every step is a listed rate and
    that the product is above 1 (beyond rounding noise).

Aim for:  Bellman–Ford on weights -log(rate): a product > 1 is a negative cycle.
Hint:     Start every distance at 0 and relax n times, remembering each node's predecessor. If round n
          still relaxes edge u → v, walk predecessors back n steps from v to land inside the cycle,
          then follow predecessors until you return to that node.
"""


def find_arbitrage(rates: list[list]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _profitable(rates):
    import math
    names = sorted({r[0] for r in rates} | {r[1] for r in rates})
    idx = {c: i for i, c in enumerate(names)}
    n = len(names)
    INF = float("inf")
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, rate in rates:
        d[idx[a]][idx[b]] = min(d[idx[a]][idx[b]], -math.log(rate))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return any(d[i][i] < -1e-9 for i in range(n))


def CHECK(got, expected, args):
    rates = args[0]
    if not _profitable(rates):
        return got == []
    if not isinstance(got, list) or len(got) < 3 or got[0] != got[-1]:
        return False
    best = {}
    for a, b, r in rates:
        best[(a, b)] = max(best.get((a, b), 0), r)
    product = 1.0
    for a, b in zip(got, got[1:]):
        if (a, b) not in best:
            return False
        product *= best[(a, b)]
    return product > 1 + 1e-9


def _market(rng, n, profitable):
    import math
    names = [f"C{i}" for i in range(n)]
    value = [rng.uniform(0.5, 2.0) for _ in range(n)]
    rates = []
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < 0.6:
                rates.append([names[i], names[j], round(value[i] / value[j] * rng.uniform(0.95, 0.999), 6)])
    if profitable and n > 1:
        a, b = rng.sample(range(n), 2)
        rates.append([names[a], names[b], round(value[a] / value[b] * 1.03, 6)])
        rates.append([names[b], names[a], round(value[b] / value[a] * 1.0, 6)])
    return rates


def _describe(rates):
    return "a profitable cycle" if _profitable(rates) else []


def _cases():
    import random
    rng = random.Random(320)
    out = [_market(rng, rng.randint(2, 6), rng.random() < 0.5) for _ in range(8)]
    out.append(_market(rng, 40, True))
    return [((r,), _describe(r)) for r in out]


_EX = [["USD", "EUR", 0.9], ["EUR", "GBP", 0.9], ["GBP", "USD", 1.3]]
TESTS = [((_EX,), _describe(_EX)), (([["USD", "EUR", 0.9], ["EUR", "USD", 1.1]],), _describe([["USD", "EUR", 0.9], ["EUR", "USD", 1.1]])),
         (([["A", "B", 2.0], ["B", "A", 0.5]],), []), (([],), [])] + _cases()
