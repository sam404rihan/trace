def combinations(n: int, k: int) -> list[list[int]]:
    out, path = [], []

    def backtrack(start):
        need = k - len(path)
        if need == 0:
            out.append(path[:])                 # record a copy: path keeps changing
            return
        for x in range(start, n - need + 2):    # prune: leave room for the rest of the picks
            path.append(x)                      # choose
            backtrack(x + 1)                    # explore
            path.pop()                          # un-choose

    backtrack(1)
    return out
