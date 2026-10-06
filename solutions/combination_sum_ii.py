def combination_sum_ii(candidates, target):
    c = sorted(candidates)
    out, path = [], []

    def backtrack(start, left):
        if left == 0:
            out.append(path[:])
            return
        for i in range(start, len(c)):
            if i > start and c[i] == c[i - 1]:
                continue                    # same value at the same depth = a duplicate branch
            if c[i] > left:
                break                       # sorted: everything after is too big too
            path.append(c[i])
            backtrack(i + 1, left - c[i])   # i + 1: each candidate at most once
            path.pop()

    backtrack(0, target)
    return out
