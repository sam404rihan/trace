def character_replacement(s: str, k: int) -> int:
    counts, left, max_count, best = {}, 0, 0, 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        max_count = max(max_count, counts[ch])
        while (right - left + 1) - max_count > k:      # too many letters to repaint
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
