"""
Minimum Window Substring                                                        [hard]

Return the shortest substring of s that contains every character of t
(counting repeats). If several are equally short, return the leftmost one.
If there's none, return "".

Example:
    min_window("ADOBECODEBANC", "ABC")  ->  "BANC"
    min_window("a", "aa")               ->  ""

Aim for:  O(len(s) + len(t)).
Hint:     Count what t needs. Grow the window to the right, tracking how many required characters
          are fully satisfied. Once all are, shrink from the left as far as you can while it stays
          valid, recording the best window each time.
"""


def min_window(s: str, t: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, t):
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            w = s[i:j + 1]
            if all(w.count(c) >= n for c, n in need.items()):
                if not best or len(w) < len(best):
                    best = w
                break
    return best


def _cases():
    import random
    rng = random.Random(51)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 16)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 3)))
        out.append(((s, t), _brute(s, t)))
    return out


TESTS = [(("ADOBECODEBANC", "ABC"), "BANC"), (("a", "a"), "a"), (("a", "aa"), ""), (("ab", "b"), "b"),
         (("aaflslflsldkalskaaa", "aaa"), "aaa")] + _cases()
