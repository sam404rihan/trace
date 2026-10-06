def repeated_dna(s: str) -> list[str]:
    value = {"A": 0, "C": 1, "G": 2, "T": 3}
    seen, repeated, code = set(), set(), 0
    for i, ch in enumerate(s):
        code = ((code << 2) | value[ch]) & 0xFFFFF     # rolling 20-bit code of the last 10 letters
        if i >= 9:
            if code in seen:
                repeated.add(s[i - 9:i + 1])
            seen.add(code)
    return sorted(repeated)
