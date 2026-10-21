"""
Cracking the Safe                                                             [hard]

A safe's password is n digits long, each digit from 0 to k - 1. The safe checks
the LAST n digits you typed after every keypress. Return the shortest string of
digits that is guaranteed to open it: one that contains every possible
password as a substring. Any shortest answer is accepted. (k**n <= 4096.)

Example:
    cracking_safe(1, 2)  ->  "01"         (or "10")
    cracking_safe(2, 2)  ->  "00110"      contains 00, 01, 11, 10   (others work too)

Aim for:  O(k^n) with an Eulerian circuit (a de Bruijn sequence). The shortest length is always
          k^n + n - 1: each new keypress adds exactly one new password.
Hint:     Make every (n-1)-digit string a node. Typing digit d at node u moves to node
          (u + d)[1:], and "uses" the password u + d: that's an edge. Each password is one edge,
          and every node has k edges in and k out, so a circuit through every edge exists.
          Hierholzer's algorithm (DFS, append the edge's digit after its subtree is done) finds
          it. Start from "0" * (n - 1) and put that start in front of the digits.
"""


def cracking_safe(n: int, k: int) -> str:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected, args):
    n, k = args
    if not isinstance(got, str) or len(got) != k ** n + n - 1:
        return False
    if any(not ch.isdigit() or int(ch) >= k for ch in got):
        return False
    return len({got[i:i + n] for i in range(len(got) - n + 1)}) == k ** n


def _describe(n, k):
    return f"a string of length {k ** n + n - 1} containing all {k ** n} passwords"


USES = ["graph.euler"]

TESTS = [((n, k), _describe(n, k)) for n, k in
         [(1, 1), (1, 2), (2, 2), (1, 10), (3, 2), (2, 3), (4, 2), (3, 4), (2, 10), (4, 5), (12, 2), (4, 8), (3, 10)]]
