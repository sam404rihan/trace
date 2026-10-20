def stream_matches(words: list[str], letters: str) -> list[bool]:
    # A trie of the words written backwards. Each new letter walks back through the
    # stream only while the trie still has a path, so most walks stop after a few steps.
    root = {}
    for w in words:
        node = root
        for ch in reversed(w):
            node = node.setdefault(ch, {})
        node["$"] = True                    # a whole word ends here
    out = []
    for i in range(len(letters)):
        node, j, hit = root, i, False
        while j >= 0 and letters[j] in node:
            node = node[letters[j]]
            if "$" in node:
                hit = True
                break
            j -= 1
        out.append(hit)
    return out
