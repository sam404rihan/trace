def palindrome_partition(s: str) -> list[list[str]]:
    out, path = [], []

    def backtrack(start):
        if start == len(s):
            out.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:        # only palindromic pieces may be chosen
                path.append(piece)
                backtrack(end)
                path.pop()

    backtrack(0)
    return out
