from collections import Counter


def top_visitors(log_lines: list[str], k: int) -> list[tuple[str, int]]:
    # One pass to count (O(n)), then sort only the distinct IPs (O(u log u)).
    counts = Counter()
    for line in log_lines:
        parts = line.split()
        if len(parts) == 4:
            counts[parts[0]] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
