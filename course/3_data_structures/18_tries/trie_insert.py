"""
Insert into a trie                                                          [snippet]

A trie made of plain dicts: each node maps a letter to the next node, and a
node where a word ends has the key "$" set to True. Insert `word` into
`root` and return root.

Example:
    trie_insert({}, "hi")   ->  {"h": {"i": {"$": True}}}

    trie_insert({"h": {"i": {"$": True}}}, "he")
    ->  {"h": {"i": {"$": True}, "e": {"$": True}}}       "h" is shared

Hint:     node = root; for ch in word: node = node.setdefault(ch, {})
          then node["$"] = True. setdefault creates the child only if it's missing.
"""


def trie_insert(root: dict, word: str) -> dict:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (({}, "hi"), {"h": {"i": {"$": True}}}),
    (({"h": {"i": {"$": True}}}, "he"), {"h": {"i": {"$": True}, "e": {"$": True}}}),
    (({"c": {"a": {"t": {"$": True}}}}, "ca"), {"c": {"a": {"t": {"$": True}, "$": True}}}),
    (({"a": {"$": True}}, "a"), {"a": {"$": True}}),
    (({}, ""), {"$": True}),
]
