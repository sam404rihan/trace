def check_inclusion(s1: str, s2: str) -> bool:
    k = len(s1)
    if k > len(s2):
        return False
    need, window = Counter(s1), Counter(s2[:k])
    if window == need:
        return True
    for right in range(k, len(s2)):
        window[s2[right]] += 1                  # one in
        window[s2[right - k]] -= 1              # one out
        if window[s2[right - k]] == 0:
            del window[s2[right - k]]
        if window == need:
            return True
    return False
