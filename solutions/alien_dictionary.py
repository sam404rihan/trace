def alien_dictionary(words: list[str]) -> str:
    letters = {c for w in words for c in w}
    after = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:                          # first difference = one ordering rule
                if y not in after[x]:
                    after[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""                       # "abc" before "ab" can't be sorted
    ready = deque(c for c in letters if indeg[c] == 0)
    order = []
    while ready:                                # Kahn's algorithm
        c = ready.popleft()
        order.append(c)
        for d in after[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                ready.append(d)
    return "".join(order) if len(order) == len(letters) else ""
