def group_by_ends(words: list[str]) -> list[list[str]]:
    # The key is what every word in a group shares. Dicts keep insertion order. O(n).
    groups = {}
    for w in words:
        groups.setdefault((w[0], w[-1]), []).append(w)
    return list(groups.values())
