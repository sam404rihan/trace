def reverse_words(s: str) -> str:
    # split() with no argument handles every kind of extra spacing. O(n).
    return " ".join(reversed(s.split()))

    # Same thing with slicing: " ".join(s.split()[::-1])
