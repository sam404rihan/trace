def longest_unique_substring(s: str) -> int:
    # Sliding window [left, right] with no repeats. O(n).
    last_seen = {}                 # char -> most recent index
    left = best = 0
    for right, ch in enumerate(s):
        if last_seen.get(ch, -1) >= left:
            left = last_seen[ch] + 1   # jump past the previous copy
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
