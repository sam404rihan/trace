def max_matching(n_left: int, n_right: int, pairs: list[tuple[int, int]]) -> int:
    jobs = [[] for _ in range(n_left)]
    for a, j in pairs:
        jobs[a].append(j)
    owner = [-1] * n_right

    def place(a, seen):
        for j in jobs[a]:
            if j not in seen:
                seen.add(j)
                if owner[j] == -1 or place(owner[j], seen):     # free, or its holder can move
                    owner[j] = a
                    return True
        return False

    return sum(place(a, set()) for a in range(n_left))
