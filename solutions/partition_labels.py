def partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    sizes, start, end = [], 0, 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])        # this piece must reach every copy of ch
        if i == end:                    # nothing in the piece appears later: cut here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
