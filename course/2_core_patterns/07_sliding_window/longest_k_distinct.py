"""
Longest stretch with at most k kinds                                         [guided]

Return the length of the longest substring of `s` that contains at most `k`
different characters.

Example:
    longest_k_distinct("eceba", 2)    ->  3      "ece"
    longest_k_distinct("aabbcc", 1)   ->  2      "aa"
"""


def longest_k_distinct(s: str, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(4)
    # Long stretches over 4 letters, broken by a rare 5th: valid windows run thousands of characters.
    s = "".join("e" if rng.random() < 0.0004 else rng.choice("abcd") for _ in range(90_000))
    k = 4
    counts, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return s, k, best


_S, _K, _BEST = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Try every start position and extend to the right while the set of characters has at most k members. Keep the longest.",
        "hint": "Two loops: for start in range(n), then grow end while len(seen) <= k. O(n²), fine for now.",
        "tests": [
            (("eceba", 2), 3),
            (("aabbcc", 1), 2),
            (("aabbcc", 2), 4),
            (("abaccc", 2), 4),
        ],
    },
    {
        "title": "Edges",
        "text": "k = 0 allows nothing. k bigger than the number of different characters allows the whole string. The empty string gives 0.",
        "hint": "If you handle these through the general rule rather than special cases, they usually just work.",
        "tests": [
            (("abc", 0), 0),
            (("abc", 5), 3),
            (("", 2), 0),
            (("aaaa", 1), 4),
        ],
    },
    {
        "title": "Slide, don't restart",
        "text": "On a 90,000-character string, restarting at every position redoes almost all the work. Keep one window "
                "[left, right] and a dict of character counts. Grow right every step. While there are more than k keys, "
                "shrink from the left, deleting a key when its count reaches 0.",
        "hint": "Both left and right only move forward, so it's O(n) overall, even with a while inside a for.",
        "tests": [
            (("ababffzzeee", 3), 7),
            ((_S, _K), _BEST),
        ],
    },
]
