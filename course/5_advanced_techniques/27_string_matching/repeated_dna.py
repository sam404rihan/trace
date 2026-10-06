"""
Repeated DNA Sequences                                                        [medium]

s uses the letters A, C, G, T. Return every 10-letter substring that occurs
more than once, sorted alphabetically.

Example:
    repeated_dna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")  ->  ["AAAAACCCCC", "CCCCCAAAAA"]

Aim for:  O(n). A set of seen windows works, and a 20-bit rolling encoding (2 bits per letter)
          makes each step O(1) without building new strings.
Hint:     Slide a window of 10. Keep `seen` and `repeated` sets. With bits: code = ((code << 2) | v)
          & 0xFFFFF, where v maps A, C, G, T to 0..3.
"""


def repeated_dna(s: str) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    counts = {}
    for i in range(len(s) - 9):
        counts[s[i:i + 10]] = counts.get(s[i:i + 10], 0) + 1
    return sorted(w for w, c in counts.items() if c > 1)


def _cases():
    import random
    rng = random.Random(214)
    out = []
    for n in (12, 30, 60, 200):
        s = "".join(rng.choice("AC") for _ in range(n))
        out.append(((s,), _brute(s)))
    big = "".join(rng.choice("ACGT") for _ in range(200_000))
    out.append(((big,), _brute(big)))
    return out


TESTS = [(("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",), ["AAAAACCCCC", "CCCCCAAAAA"]), (("AAAAAAAAAAAAA",), ["AAAAAAAAAA"]),
         (("ACGT",), [])] + _cases()
