def shortest_palindrome(s: str) -> str:
    combined = s + "#" + s[::-1]                # "#" can't appear in s, so borders can't cross it
    pi, k = [0] * len(combined), 0
    for i in range(1, len(combined)):
        while k and combined[i] != combined[k]:
            k = pi[k - 1]
        if combined[i] == combined[k]:
            k += 1
        pi[i] = k
    keep = pi[-1]                               # length of the longest palindromic prefix
    return s[keep:][::-1] + s
