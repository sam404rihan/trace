"""
Cheapest travel passes                                                        [build]

You know which days of the year you'll ride the train (`days`, sorted, each
1..365). A 1-day pass costs costs[0], a 7-day pass costs[1] and a 30-day pass
costs[2]. A pass bought on day d covers d through d + length − 1. Return the
minimum total cost to cover every travel day, and the passes to buy.

    travel_passes([1, 4, 6, 7, 8, 20], [2, 7, 15])
    ->  (11, [(1, 1), (4, 7), (20, 1)])
        a 1-day pass on day 1, a 7-day pass on day 4 (covers 4-10), a 1-day pass on day 20

Return (total, passes), where passes is a list of (start_day, length) in order of
start day.

Rules:
  - Any cheapest plan is accepted. The tests check that your passes cost exactly
    `total`, cover every travel day, and that `total` is the minimum.

Hint:     dp[d] = cheapest way to cover every travel day up to day d. On a day you don't
          travel, dp[d] = dp[d - 1]. On a travel day, try each pass ending today:
          dp[d] = min(dp[d-1] + c1, dp[d-7] + c7, dp[d-30] + c30), using 0 for negative days.
          Record which choice won, then walk back from day 365 to list the passes.
"""


def travel_passes(days: list[int], costs: list[int]) -> tuple[int, list[tuple[int, int]]]:
    raise NotImplementedError  # replace this line with your solution


def _cheapest(days, costs):
    travel = set(days)
    dp = [0] * 366
    for d in range(1, 366):
        if d not in travel:
            dp[d] = dp[d - 1]
        else:
            dp[d] = min(dp[max(0, d - 1)] + costs[0], dp[max(0, d - 7)] + costs[1], dp[max(0, d - 30)] + costs[2])
    return dp[365]


def CHECK(got, expected, args):
    days, costs = args
    best = _cheapest(days, costs)
    if not (isinstance(got, (tuple, list)) and len(got) == 2):
        return False
    total, passes = got
    if total != best:
        return False
    price = {1: costs[0], 7: costs[1], 30: costs[2]}
    try:
        if sum(price[length] for _, length in passes) != total:
            return False
        covered = {d for start, length in passes for d in range(start, start + length)}
    except (KeyError, TypeError, ValueError):
        return False
    return all(d in covered for d in days)


def _big():
    import random
    rng = random.Random(31)
    return sorted(rng.sample(range(1, 366), 160)), [3, 14, 40]


_CASES = [
    ([1, 4, 6, 7, 8, 20], [2, 7, 15]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15]),
    ([5], [4, 3, 10]),
    ([1, 365], [2, 7, 15]),
    (list(range(1, 366)), [2, 7, 15]),
    _big(),
]

TESTS = [(case, f"(cost {_cheapest(*case)}, any cheapest plan)") for case in _CASES]
