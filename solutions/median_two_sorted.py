def median_two_sorted(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        a, b = b, a                             # search the shorter array
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while True:
        i = (lo + hi) // 2                      # take i from a...
        j = half - i                            # ...and the rest of the left half from b
        a_left = a[i - 1] if i > 0 else float("-inf")
        a_right = a[i] if i < m else float("inf")
        b_left = b[j - 1] if j > 0 else float("-inf")
        b_right = b[j] if j < n else float("inf")
        if a_left <= b_right and b_left <= a_right:
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
