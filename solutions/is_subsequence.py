def is_subsequence(s: str, t: str) -> bool:
    # One pointer per string: j walks all of s, i moves on in t only on a match. O(len(s) + len(t)).
    i = 0
    for ch in s:
        if i < len(t) and t[i] == ch:
            i += 1
    return i == len(t)
