"""
Longest Valid Parentheses                                                     [hard]

`s` contains only "(" and ")". Return the length of the longest substring that
is a well-formed (balanced) parentheses string.

Example:
    longest_valid_parentheses("(()")       ->  2      "()"
    longest_valid_parentheses(")()())")    ->  4      "()()"
    longest_valid_parentheses("")          ->  0

Aim for:  O(n) with a stack of indices.
Hint:     Push indices of "(". Keep a sentinel at the bottom of the stack: the index just before
          the current valid run (start with -1). On ")", pop. If the stack is now empty, this ")"
          can't match: push its index as the new sentinel. Otherwise the valid run ending here
          has length i - stack[-1].
"""


def longest_valid_parentheses(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    def ok(t):
        depth = 0
        for ch in t:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0
    return max((j - i for i in range(len(s)) for j in range(i + 2, len(s) + 1, 2) if ok(s[i:j])), default=0)


def _fast(s):
    stack, best = [-1], 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best


def _cases():
    import random
    rng = random.Random(32)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("()") for _ in range(rng.randint(0, 16)))
        out.append(((s,), _brute(s)))
    big = "".join(rng.choice(["()", "(())", "(", ")"]) for _ in range(30_000))
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (("(()",), 2),
    ((")()())",), 4),
    (("",), 0),
    (("()(())",), 6),
    (("()(()",), 2),
    (("((((",), 0),
    (("(()())",), 6),
    ((")(",), 0),
] + _cases()
