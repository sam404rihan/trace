def pick_talks(talks: list[tuple[str, int, int]]) -> list[str]:
    picked, last_end = [], float("-inf")
    # Earliest end first leaves the most room for everything after it.
    for name, start, end in sorted(talks, key=lambda t: (t[2], t[0])):
        if start >= last_end:
            picked.append(name)
            last_end = end
    return picked
