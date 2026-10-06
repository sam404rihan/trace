def palindromic_substrings(s: str) -> int:
    count = 0
    for centre in range(2 * len(s) - 1):
        lo, hi = centre // 2, centre // 2 + centre % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            count += 1                      # s[lo:hi+1] is one more palindrome
            lo, hi = lo - 1, hi + 1
    return count
