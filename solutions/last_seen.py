def last_seen(items: list) -> dict:
    # Overwriting means the last index wins. A dict comprehension does the same:
    #   return {x: i for i, x in enumerate(items)}
    seen = {}
    for i, x in enumerate(items):
        seen[x] = i
    return seen
