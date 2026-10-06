from collections import defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    # Anagrams have the same sorted letters, so that's the key. O(n · k log k).
    groups = defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())

    # O(n · k) variant: use a tuple of 26 letter counts as the key instead.
