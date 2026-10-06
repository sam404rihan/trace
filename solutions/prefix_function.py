def prefix_function(s: str) -> list[int]:
    pi, k = [0] * len(s), 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]           # fall back to the next shorter border
        if s[i] == s[k]:
            k += 1                  # the border grows by one
        pi[i] = k
    return pi
