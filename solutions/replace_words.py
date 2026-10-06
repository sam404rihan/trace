def replace_words(roots: list[str], sentence: str) -> str:
    # Trie of the roots; each word walks down until it hits the end of a root.
    trie = {}
    for root in roots:
        node = trie
        for ch in root:
            node = node.setdefault(ch, {})
        node["$"] = True

    def shortest_root(word):
        node = trie
        for i, ch in enumerate(word):
            if ch not in node:
                break
            node = node[ch]
            if "$" in node:
                return word[: i + 1]     # the first root found is the shortest
        return word

    return " ".join(shortest_root(w) for w in sentence.split())
