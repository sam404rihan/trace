def stickers_to_spell(stickers: list[str], target: str) -> int:
    t = len(target)
    full = (1 << t) - 1
    counts = [Counter(s) for s in stickers]
    best = [-1] * (1 << t)          # best[mask]: fewest stickers to cover these target positions
    best[0] = 0
    queue = deque([0])
    while queue:                    # BFS: every step uses one more sticker
        mask = queue.popleft()
        if mask == full:
            return best[mask]
        first = next(i for i in range(t) if not mask >> i & 1)
        for count in counts:
            if target[first] not in count:
                continue            # it must be covered by some sticker; try those first
            left = count.copy()
            nxt = mask
            for i in range(t):
                if not nxt >> i & 1 and left[target[i]] > 0:
                    left[target[i]] -= 1
                    nxt |= 1 << i
            if best[nxt] == -1:
                best[nxt] = best[mask] + 1
                queue.append(nxt)
    return -1
