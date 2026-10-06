"""
Line diff, like git diff                                                      [build]

Compare two versions of a file (lists of lines) and return a diff: every line
from either version, in order, prefixed with

    "  " (kept: in both),   "- " (only in the old version),   "+ " (only in the new version)

The diff must be minimal: it keeps as many lines as possible, which is the
longest common subsequence of the two files.

    diff_lines(["a", "b", "c", "d"], ["a", "c", "d", "e"])
    ->  ["  a", "- b", "  c", "  d", "+ e"]

Rules:
  - Any minimal diff is accepted. The tests check three things: the kept and
    removed lines rebuild the old file, the kept and added lines rebuild the
    new file, and the number of kept lines equals the LCS length.

Hint:     Build the LCS table dp[i][j] for old[:i] and new[:j]. Then walk from (0, 0)
          using a suffix table, or backwards from the end: matching lines are kept.
          Otherwise step towards the larger neighbour, emitting "- " or "+ ".
"""


def diff_lines(old: list[str], new: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _lcs(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def CHECK(got, expected, args):
    old, new = args
    if not isinstance(got, list) or any(not isinstance(l, str) or l[:2] not in ("  ", "- ", "+ ") for l in got):
        return False
    rebuilt_old = [l[2:] for l in got if l[:2] in ("  ", "- ")]
    rebuilt_new = [l[2:] for l in got if l[:2] in ("  ", "+ ")]
    kept = sum(1 for l in got if l[:2] == "  ")
    return rebuilt_old == old and rebuilt_new == new and kept == _lcs(old, new)


def _big():
    import random
    rng = random.Random(33)
    base = [f"line {rng.randint(0, 60)}" for _ in range(500)]
    new = [l for l in base if rng.random() > 0.1]
    for _ in range(50):
        new.insert(rng.randint(0, len(new)), f"added {rng.randint(0, 99)}")
    return base, new


_CASES = [
    (["a", "b", "c", "d"], ["a", "c", "d", "e"]),
    (["same", "same"], ["same", "same"]),
    ([], ["x", "y"]),
    (["x", "y"], []),
    (["def f():", "    return 1", ""], ["def f():", "    print('hi')", "    return 2", ""]),
    (["a", "b", "a", "b"], ["b", "a", "b", "a"]),
    _big(),
]

TESTS = [(case, f"a minimal diff keeping {_lcs(*case)} line(s)") for case in _CASES]
