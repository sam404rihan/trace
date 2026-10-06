"""
Remove Invalid Parentheses                                                    [hard]

`s` contains "(", ")" and lowercase letters. Remove the FEWEST parentheses
needed to make it valid (balanced). Return every distinct valid result you can
get with that minimum number of removals, sorted.

Example:
    remove_invalid_parentheses("()())()")   ->  ["(())()", "()()()"]
    remove_invalid_parentheses("(a)())()")  ->  ["(a())()", "(a)()()"]
    remove_invalid_parentheses(")(")        ->  [""]

Aim for:  backtracking that knows in advance how many "(" and ")" to remove.
Hint:     One left-to-right scan tells you how many ")" are unmatched and how many "(" are left
          open at the end: exactly those must go. Then recurse over the string, at each
          parenthesis choosing keep or remove (while you still have removals of that kind left),
          tracking the open count so it never goes negative. Give up early when fewer "(" (or
          ")") remain than you still have to remove. Different removals can give the same
          string, so collect results in a set.
"""


def remove_invalid_parentheses(s: str) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    """BFS by number of removals."""
    def ok(t):
        depth = 0
        for ch in t:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth < 0:
                    return False
        return depth == 0
    level = {s}
    while level:
        good = sorted(t for t in level if ok(t))
        if good:
            return good
        level = {t[:i] + t[i + 1:] for t in level for i in range(len(t)) if t[i] in "()"}
    return [""]


def _cases():
    import random
    rng = random.Random(301)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("(()))x") for _ in range(rng.randint(0, 10)))
        out.append(((s,), _brute(s)))
    # 19 of the 20 "(" must go. Trying removals level by level would build C(20, 10) strings.
    s = "(a" * 20 + ")"
    out.append(((s,), sorted("a" * i + "(" + "a" * (20 - i) + ")" for i in range(20))))
    return out


TESTS = [
    (("()())()",), ["(())()", "()()()"]),
    (("(a)())()",), ["(a())()", "(a)()()"]),
    ((")(",), [""]),
    (("",), [""]),
    (("abc",), ["abc"]),
    (("((",), [""]),
    (("(()",), ["()"]),
    ((")a)",), ["a"]),
] + _cases()
