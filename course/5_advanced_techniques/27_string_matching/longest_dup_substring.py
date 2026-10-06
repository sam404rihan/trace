"""
Longest Duplicate Substring                                                   [hard]

Return the longest substring of `s` that occurs at least twice (the two
occurrences may overlap). If several are equally long, return the one whose
first occurrence starts earliest. If no substring repeats, return "".

Example:
    longest_dup_substring("banana")   ->  "ana"      at 1 and 3, overlapping
    longest_dup_substring("abcd")     ->  ""
    longest_dup_substring("aabcaabdaab")  ->  "aab"

Aim for:  O(n log n) on average: binary search on the length + rolling hash.
Hint:     If a repeat of length L exists, one of length L - 1 does too, so binary search on L.
          To test a length, slide a polynomial rolling hash over every window of length L and
          look for a hash seen before; confirm a match by comparing the actual substrings (two
          different strings can share a hash). To pick the earliest-starting answer at the
          final length, record the smallest start whose window appears again later.
"""


def longest_dup_substring(s: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    n = len(s)
    for length in range(n - 1, 0, -1):
        seen, best = {}, None
        for i in range(n - length + 1):
            w = s[i:i + length]
            if w in seen and (best is None or seen[w] < best):
                best = seen[w]
            seen.setdefault(w, i)
        if best is not None:
            return s[best:best + length]
    return ""


def _repeat_start(s, length):
    """Smallest i such that s[i:i + length] occurs again later, or None (set-based, fast enough)."""
    first, best = {}, None
    for i in range(len(s) - length + 1):
        w = s[i:i + length]
        if w in first:
            j = first[w]
            if best is None or j < best:
                best = j
        else:
            first[w] = i
    return best


def _fast(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _repeat_start(s, mid) is not None:
            lo = mid
        else:
            hi = mid - 1
    if lo == 0:
        return ""
    i = _repeat_start(s, lo)
    return s[i:i + lo]


def _cases():
    import random
    rng = random.Random(1044)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 14)))
        out.append(((s,), _brute(s)))
    big = "".join(rng.choice("acgt") for _ in range(8_000))
    big = big[:5_000] + big[1_000:1_300] + big[5_000:]           # plant a 300-long repeat
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (("banana",), "ana"),
    (("abcd",), ""),
    (("aabcaabdaab",), "aab"),
    (("aaaaa",), "aaaa"),
    (("a",), ""),
    (("abab",), "ab"),
    (("xyzabcxyzabd",), "xyzab"),
] + _cases()
