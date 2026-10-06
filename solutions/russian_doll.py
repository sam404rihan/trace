def russian_doll(envelopes: list[list[int]]) -> int:
    # Equal widths sorted tallest first, so at most one of them can join an increasing run.
    envelopes = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    tails = []                  # tails[k]: smallest last height of an increasing run of length k + 1
    for _, h in envelopes:
        i = bisect_left(tails, h)
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return len(tails)
