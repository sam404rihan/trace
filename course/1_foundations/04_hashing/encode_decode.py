"""
Encode and Decode Strings                                                    [medium]

Write encode(strs), which packs a list of strings into ONE string, and
decode(s), which unpacks it into exactly the same list. The strings can contain
anything: commas, "#", digits, spaces, newlines, or nothing at all.

The tests call encode_decode at the bottom. Leave that function as it is.

Example:
    decode(encode(["lint", "code", "", "4#a"]))  ->  ["lint", "code", "", "4#a"]

Aim for:  O(total length). No separator character is safe on its own, because any
          character can appear inside a string.
Hint:     Length-prefix each string: "4#lint4#code0#3#4#a". To decode, read digits up to "#",
          then take exactly that many characters. The length says where the string ends,
          whatever it contains.
"""


def encode(strs: list[str]) -> str:
    raise NotImplementedError  # replace this line with your solution


def decode(s: str) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def encode_decode(strs: list[str]) -> list[str]:
    # Don't change this: it encodes two lists and decodes them in a different order.
    a, b = encode(strs), encode(["", "x"])
    if not isinstance(a, str):
        raise TypeError("encode must return a str")
    decode(b)
    return decode(a)


TESTS = [
    ((["lint", "code", "", "4#a"],), ["lint", "code", "", "4#a"]),
    (([],), []),
    (([""],), [""]),
    (([",", "#", "##", "3#abc"],), [",", "#", "##", "3#abc"]),
    ((["multi\nline", "  spaces  ", "ünïcødé ✓"],), ["multi\nline", "  spaces  ", "ünïcødé ✓"]),
    ((["x" * 1000, "12345", "0#"],), ["x" * 1000, "12345", "0#"]),
]
