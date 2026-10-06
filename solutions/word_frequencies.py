from collections import Counter


def word_frequencies(text: str) -> list[tuple[str, int]]:
    # Clean each word once, count in one pass (O(n)), then sort only the distinct words.
    words = (raw.lower().strip(".,!?;:\"'()") for raw in text.split())
    counts = Counter(w for w in words if w)
    # Sort key: count descending (negate it), then the word alphabetically.
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
