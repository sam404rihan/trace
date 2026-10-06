def scramble_string(s: str, t: str) -> bool:
    @cache
    def can(a, b):
        if a == b:
            return True
        if sorted(a) != sorted(b):              # different letters can never match
            return False
        for k in range(1, len(a)):
            if can(a[:k], b[:k]) and can(a[k:], b[k:]):         # cut at k, parts kept in order
                return True
            if can(a[:k], b[-k:]) and can(a[k:], b[:-k]):       # cut at k, parts swapped
                return True
        return False

    return can(s, t)
