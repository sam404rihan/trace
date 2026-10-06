def trie_insert(root: dict, word: str) -> dict:
    node = root
    for ch in word:
        node = node.setdefault(ch, {})   # follow the shared prefix, create only what's missing
    node["$"] = True                     # mark: a word ends here
    return root
