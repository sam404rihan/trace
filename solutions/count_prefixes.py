def count_prefixes(words: list[str], prefixes: list[str]) -> list[int]:
    # Trie of dicts; "#" at each node counts the words passing through it.
    root = {"#": 0}
    for word in words:
        node = root
        node["#"] += 1                   # every word "starts with" the empty prefix
        for ch in word:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1

    def count(prefix):
        node = root
        for ch in prefix:
            if ch not in node:
                return 0
            node = node[ch]
        return node["#"]

    return [count(p) for p in prefixes]

    # Hash-map alternative: count every prefix of every word in a Counter.
    # Simpler, but stores a copy of each prefix string.
