def min_palindrome_cuts(s: str) -> int:
    n = len(s)
    pal = [[False] * n for _ in range(n)]       # pal[i][j]: s[i..j] is a palindrome
    cuts = [0] * n                              # cuts[j]: fewest cuts for s[0..j]
    for j in range(n):
        best = j                                # worst case: cut between every letter
        for i in range(j + 1):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
                best = 0 if i == 0 else min(best, cuts[i - 1] + 1)   # last piece is s[i..j]
        cuts[j] = best
    return cuts[-1] if n else 0
