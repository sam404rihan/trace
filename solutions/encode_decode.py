def encode(strs: list[str]) -> str:
    # Length-prefix every string, so its contents can never be mistaken for a separator.
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s: str) -> list[str]:
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)              # the length ends at the first "#"
        n = int(s[i:j])
        out.append(s[j + 1:j + 1 + n])   # then take exactly n characters
        i = j + 1 + n
    return out


def encode_decode(strs: list[str]) -> list[str]:
    a, b = encode(strs), encode(["", "x"])
    if not isinstance(a, str):
        raise TypeError("encode must return a str")
    decode(b)
    return decode(a)
