import bisect


def autocomplete(words: list[str], queries: list[str]) -> list[list[str]]:
    words = sorted(set(words))          # sort once: words sharing a prefix become neighbours
    out = []
    for q in queries:
        i = bisect.bisect_left(words, q)    # first word >= q is where the prefix block starts
        out.append([w for w in words[i:i + 3] if w.startswith(q)])
    return out
