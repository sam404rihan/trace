def distinct_subsequences(s: str, t: str) -> int:
    ways = [1] + [0] * len(t)                   # ways[j]: ways to form t[:j] so far
    for ch in s:
        for j in range(len(t), 0, -1):          # descending: each ch used at most once per way
            if t[j - 1] == ch:
                ways[j] += ways[j - 1]
    return ways[len(t)]
