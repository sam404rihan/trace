def travel_passes(days: list[int], costs: list[int]) -> tuple[int, list[tuple[int, int]]]:
    travel = set(days)
    lengths = (1, 7, 30)
    dp = [0] * 366                 # dp[d] = cheapest cover of every travel day up to day d
    choice = [None] * 366          # which pass length ends at day d in the best plan
    for d in range(1, 366):
        if d not in travel:
            dp[d] = dp[d - 1]      # nothing to cover today
            continue
        dp[d], choice[d] = min((dp[max(0, d - L)] + c, L) for L, c in zip(lengths, costs))

    passes, d = [], 365
    while d > 0:                   # walk the choices backwards to recover the plan
        if choice[d] is None:
            d -= 1
            continue
        L = choice[d]
        passes.append((max(1, d - L + 1), L))
        d -= L
    return dp[365], passes[::-1]
