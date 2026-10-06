def concatenated_words(words: list[str]) -> list[str]:
    root = {}
    for w in words:                     # a trie of all words; "$" marks a word's end
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def is_concatenated(w):
        can = [False] * (len(w) + 1)    # can[i]: w[:i] splits into list words
        can[0] = True
        for i in range(len(w)):
            if not can[i]:
                continue
            node = root
            for j in range(i, len(w)):  # every list word that starts at i
                node = node.get(w[j])
                if node is None:
                    break
                if "$" in node and not (i == 0 and j == len(w) - 1):    # not the word itself
                    can[j + 1] = True
        return can[len(w)]

    return [w for w in words if is_concatenated(w)]
