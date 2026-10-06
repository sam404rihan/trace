def min_window_subsequence(s: str, t: str) -> str:
    best_start, best_len = 0, float("inf")
    i = 0
    while i < len(s):
        k = 0
        while i < len(s):                   # forward: match all of t in order
            if s[i] == t[k]:
                k += 1
                if k == len(t):
                    break
            i += 1
        if k < len(t):
            break
        end = i
        k = len(t) - 1
        while k >= 0:                       # backward: the latest start that still fits t
            if s[i] == t[k]:
                k -= 1
            i -= 1
        start = i + 1
        if end - start + 1 < best_len:
            best_start, best_len = start, end - start + 1
        i = start + 1                       # windows starting later are found from here
    return "" if best_len == float("inf") else s[best_start:best_start + best_len]
