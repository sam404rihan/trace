from functools import cache


def word_break(s: str, words: list[str]) -> bool:
    # can[i] = s[:i] can be built from words. O(n²) substring checks.
    word_set = set(words)
    can = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if can[j] and s[j:i] in word_set:
                can[i] = True
                break
    return can[len(s)]


def word_break_memo(s: str, words: list[str]) -> bool:
    # Top-down: same recursion you'd write first, plus @cache on the start index.
    word_set = set(words)

    @cache
    def from_index(i):
        if i == len(s):
            return True
        return any(s[i:j] in word_set and from_index(j) for j in range(i + 1, len(s) + 1))

    return from_index(0)
