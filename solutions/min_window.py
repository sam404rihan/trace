def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)                    # characters of t not yet covered (with multiplicity)
    left = 0
    best = (float("inf"), 0, 0)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                   # negative = surplus in the window
        if missing == 0:
            while need[s[left]] < 0:    # drop surplus characters from the left
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1          # give up the leftmost required char and keep searching
            missing += 1
            left += 1
    return s[best[1]:best[2]] if best[0] != float("inf") else ""
