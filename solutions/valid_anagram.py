def valid_anagram(s: str, t: str) -> bool:
    # Count letters up for s and down for t; every count must end at zero. O(n).
    if len(s) != len(t):
        return False
    counts = {}
    for a, b in zip(s, t):
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) - 1
    return all(c == 0 for c in counts.values())

    # Shorter: from collections import Counter; return Counter(s) == Counter(t)
    # Also fine: return sorted(s) == sorted(t)   (O(n log n))
