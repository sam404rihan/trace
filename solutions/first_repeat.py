def first_repeat(items: list):
    # Check before adding, so the moment x is already in the set, it's the first repeat.
    seen = set()
    for x in items:
        if x in seen:
            return x
        seen.add(x)
    return None
