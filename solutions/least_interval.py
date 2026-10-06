def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks).values()
    top = max(counts)
    tied = sum(1 for c in counts if c == top)
    frame = (top - 1) * (n + 1) + tied      # the most frequent letter forces this many slots
    return max(frame, len(tasks))           # enough other tasks fill every idle gap
