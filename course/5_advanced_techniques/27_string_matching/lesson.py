"""
# String matching

Searching for a pattern of length m in a text of length n the obvious way can take
O(n · m). KMP and rolling hashes do it in O(n + m) by never re-examining text
you've already matched.

## Use it when
- Find every occurrence of a pattern, or check whether a string repeats itself
- Longest prefix that is also a suffix, or shortest palindrome by adding characters in front
- Duplicate substrings, or comparing many substrings quickly (rolling hash)

## Prefix function (KMP's failure table)
pi[i] = length of the longest proper prefix of s[:i+1] that is also a suffix of it.
```
pi = [0] * len(s); k = 0
for i in range(1, len(s)):
    while k and s[i] != s[k]: k = pi[k - 1]     # fall back to a shorter border
    if s[i] == s[k]: k += 1
    pi[i] = k
```
Search: run the same loop over pattern + "#" + text. Wherever pi == len(pattern), there's a match.

## Rolling hash (Rabin–Karp)
```
h = (h * B + ord(ch)) % M                       # append a character
h = (h - ord(old) * B**(L-1)) % M               # drop the first character of the window
```
Equal hashes are probably equal strings. Compare the real substrings to be sure, or use two moduli.

## Common mistakes
- Using a separator character that can appear in the text
- Forgetting that pi values are LENGTHS, so the matching index is pi - 1
- Negative values after subtracting in modular hashing: in Python, % M fixes that
"""


def prefix_function(s):
    pi, k = [0] * len(s), 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


print("pi of 'abacaba':", prefix_function("abacaba"))    # [0, 0, 1, 0, 1, 2, 3]
p, text = "aba", "abababa"
pi = prefix_function(p + "#" + text)
print("matches of 'aba':", [i - 2 * len(p) for i, v in enumerate(pi) if v == len(p)])   # [0, 2, 4]
