def word_ladder(begin: str, end: str, words: list[str]) -> int:
    if end not in words:
        return 0
    L = len(begin)
    by_pattern = defaultdict(list)                  # "h*t" -> words matching it
    for w in words:
        for i in range(L):
            by_pattern[w[:i] + "*" + w[i + 1:]].append(w)
    seen, queue = {begin}, deque([(begin, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(L):
            key = word[:i] + "*" + word[i + 1:]
            for nxt in by_pattern.pop(key, ()):     # each pattern is expanded once
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0
