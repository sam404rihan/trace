def find_all(text: str, pattern: str) -> list[int]:
    m = len(pattern)
    pi, k = [0] * m, 0                      # prefix function of the pattern
    for i in range(1, m):
        while k and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    out, k = [], 0
    for i, ch in enumerate(text):           # the text is read once, never backwards
        while k and ch != pattern[k]:
            k = pi[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == m:
            out.append(i - m + 1)
            k = pi[k - 1]                   # keep going: matches may overlap
    return out
