def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    # One pointer per list; each step takes the smaller front. O(len(a) + len(b)).
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]              # one of these is empty
