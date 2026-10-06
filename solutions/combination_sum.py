def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    # Backtracking. Recurse with i (not i + 1) so a number can be reused, and
    # never look back at smaller indexes, so [2, 3] and [3, 2] aren't both built.
    candidates = sorted(candidates)
    result, path = [], []

    def explore(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                    # sorted, so everything after is too big too
            path.append(candidates[i])
            explore(i, remaining - candidates[i])
            path.pop()

    explore(0, target)
    return result
