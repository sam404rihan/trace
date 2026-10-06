def longest_dup_substring(s: str) -> str:
    n = len(s)
    MOD, BASE = (1 << 61) - 1, 131

    def repeat_start(length):
        """Smallest start of a window of this length that appears again later, or -1."""
        if length == 0:
            return 0
        power = pow(BASE, length, MOD)
        h = 0
        for ch in s[:length]:
            h = (h * BASE + ord(ch)) % MOD
        first = {h: [0]}                # hash -> starts with that hash (usually just one)
        best = -1
        for i in range(1, n - length + 1):
            h = (h * BASE + ord(s[i + length - 1]) - ord(s[i - 1]) * power) % MOD
            window = s[i:i + length]
            starts = first.setdefault(h, [])
            for j in starts:
                if s[j:j + length] == window:       # a real match, not just a hash collision
                    if best == -1 or j < best:
                        best = j
                    break
            else:
                starts.append(i)
        return best

    lo, hi = 0, n - 1                   # a repeat of length lo exists; none longer than hi
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if repeat_start(mid) != -1:
            lo = mid
        else:
            hi = mid - 1
    if lo == 0:
        return ""
    start = repeat_start(lo)
    return s[start:start + lo]
