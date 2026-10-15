def longest_k_distinct(s: str, k: int) -> int:
    counts, left, best = {}, 0, 0
    for right, ch in enumerate(s):  #@skeleton
        counts[ch] = counts.get(ch, 0) + 1          # grow: take s[right]
        while len(counts) > k:                       # too many kinds: shrink from the left  #@skeleton
            gone = s[left]
            counts[gone] -= 1
            if counts[gone] == 0:
                del counts[gone]
            left += 1  #@skeleton
        best = max(best, right - left + 1)
    return best
