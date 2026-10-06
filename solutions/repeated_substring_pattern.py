def repeated_substring_pattern(s: str) -> bool:
    n = len(s)
    pi, k = [0] * n, 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    period = n - pi[-1] if n else 0         # the smallest shift that maps s onto itself
    return n > 0 and pi[-1] > 0 and n % period == 0
