def palindrome_pairs(words: list[str]) -> list[list[int]]:
    index = {w: i for i, w in enumerate(words)}
    found = set()
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            prefix, suffix = w[:cut], w[cut:]
            # u + w with u = reversed(suffix): u + prefix + suffix reads the same both ways
            # because prefix is a palindrome sitting in the middle.
            if prefix == prefix[::-1]:
                j = index.get(suffix[::-1])
                if j is not None and j != i:
                    found.add((j, i))
            # w + u with u = reversed(prefix), when the suffix is the palindromic middle.
            if suffix == suffix[::-1]:
                j = index.get(prefix[::-1])
                if j is not None and j != i:
                    found.add((i, j))
    return [list(pair) for pair in sorted(found)]
