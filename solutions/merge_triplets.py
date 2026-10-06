def merge_triplets(triplets: list[list[int]], target: list[int]) -> bool:
    matched = set()
    for t in triplets:
        if all(x <= y for x, y in zip(t, target)):     # only "safe" triplets can be merged
            matched |= {i for i in range(3) if t[i] == target[i]}
    return len(matched) == 3
