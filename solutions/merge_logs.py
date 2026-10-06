def merge_logs(a: list[str], b: list[str]) -> list[str]:
    out, i, j = [], 0, 0
    while i < len(a) or j < len(b):
        # Take from a when b is used up, or when a's time is not later (ties prefer a).
        if j == len(b) or (i < len(a) and a[i][:8] <= b[j][:8]):
            line, i = a[i], i + 1
        else:
            line, j = b[j], j + 1
        if not out or out[-1] != line:      # skip exact repeats of the line just written
            out.append(line)
    return out
