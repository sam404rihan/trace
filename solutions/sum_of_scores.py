def sum_of_scores(s: str) -> int:
    n = len(s)
    z = [0] * n
    left = right = 0                    # s[left:right] matches s[:right - left], right is furthest
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])  # already known from the mirrored position
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                           # extend by comparing past what's known
        if i + z[i] > right:
            left, right = i, i + z[i]
    return n + sum(z)                   # the whole string scores n; z[0] stays 0
