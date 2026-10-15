"""Build the sliding window, one piece at a time"""

# Each layer is a complete program: the code so far plus a small example that prints.
# Lines new in a layer are found automatically. A trailing #@role tags a line in a reuse layer.

LAYERS = [
    {
        "title": "The loop: two edges",
        "why": """
            A window is a stretch `s[left:right + 1]`. The right edge walks every position once.
            For now `left` never moves, so the window only grows. That's the skeleton: one loop,
            two edges, and both edges only ever move right.

            Our problem: the longest stretch of `s` with at most `k` different letters.
        """,
        "code": '''
            def longest_k_distinct(s, k):
                left = 0
                for right in range(len(s)):
                    print(f"  right={right}  window={s[left:right + 1]!r}")


            longest_k_distinct("abcbbca", 2)
        ''',
        "check": {
            "question": "When the loop ends, what is the window?",
            "options": ["Just the last letter", "The whole string", "The longest valid stretch"],
            "answer": 1,
            "explain": "`left` never moved, so the window grew to cover everything. Nothing stops it from breaking the rule yet.",
        },
    },
    {
        "title": "Window state: know what's inside",
        "why": """
            To know whether the window breaks the rule (at most `k` kinds of letter), keep a count
            of what's inside. Taking a letter is one dict update, and `len(counts)` is the number of
            kinds. When the left edge moves later, we subtract instead of recounting.
        """,
        "code": '''
            def longest_k_distinct(s, k):
                counts = {}                      # letter -> copies inside the window
                left = 0
                for right in range(len(s)):
                    counts[s[right]] = counts.get(s[right], 0) + 1
                    print(f"  window={s[left:right + 1]!r}  kinds={len(counts)}")


            longest_k_distinct("abcbbca", 2)
        ''',
        "check": {
            "question": "Why keep `counts` instead of computing `len(set(s[left:right + 1]))` each step?",
            "options": [
                "It's shorter to write",
                "Updating it costs O(1) per step; rebuilding a set rescans the whole window",
                "A set can't hold letters",
            ],
            "answer": 1,
            "explain": "Rescanning the window every step makes the whole thing O(n²). Updating the counts as the edges move keeps it O(n).",
        },
    },
    {
        "title": "Shrink while the window is invalid",
        "why": """
            Once the window holds more than `k` kinds it's invalid. Drop letters from the left,
            updating `counts`, until it's valid again. Delete a letter from `counts` when its count
            reaches zero, or `len(counts)` would still count it.
        """,
        "code": '''
            def longest_k_distinct(s, k):
                counts = {}                      # letter -> copies inside the window
                left = 0
                for right in range(len(s)):
                    counts[s[right]] = counts.get(s[right], 0) + 1
                    while len(counts) > k:           # too many kinds: drop from the left
                        counts[s[left]] -= 1
                        if counts[s[left]] == 0:
                            del counts[s[left]]      # no copies left, so that kind is gone
                        left += 1
                    print(f"  window={s[left:right + 1]!r}  kinds={len(counts)}")


            longest_k_distinct("abcbbca", 2)
        ''',
        "check": {
            "question": "What goes wrong if the `while` becomes an `if`?",
            "options": [
                "Nothing: one step from the left is always enough",
                "The window can stay invalid, because dropping one letter may not remove a kind",
                "The loop never ends",
            ],
            "answer": 1,
            "explain": "A kind only disappears when its last copy leaves. When the final 'a' arrives, the window 'bcbbca' has to drop four letters before it's down to 'ca'.",
        },
    },
    {
        "title": "Record the answer",
        "why": """
            After the `while`, the window is valid again, so its length is a real candidate.
            Keep the best one and return it. That's the whole pattern: grow on the right,
            shrink while invalid, record.
        """,
        "code": '''
            def longest_k_distinct(s, k):
                counts = {}                      # letter -> copies inside the window
                left = best = 0
                for right in range(len(s)):
                    counts[s[right]] = counts.get(s[right], 0) + 1
                    while len(counts) > k:           # too many kinds: drop from the left
                        counts[s[left]] -= 1
                        if counts[s[left]] == 0:
                            del counts[s[left]]      # no copies left, so that kind is gone
                        left += 1
                    best = max(best, right - left + 1)   # valid here, so it counts
                return best


            print(longest_k_distinct("abcbbca", 2))   # 5: "bcbbc"
            print(longest_k_distinct("eceba", 2))     # 3: "ece"
        ''',
        "check": {
            "question": "Why is `best` updated after the `while`, not before it?",
            "options": [
                "It runs faster that way",
                "Before the `while`, the window may have too many kinds, so its length isn't a real answer",
                "Python needs the variable to exist first",
            ],
            "answer": 1,
            "explain": "Recording before shrinking would count windows that break the rule. After the `while`, the rule holds, so every length you record is a real answer.",
        },
    },
    {
        "title": "Same skeleton: Minimum window substring",
        "reuse": "min_window",
        "roles": {
            "state": "What the window tracks",
            "valid": "When to shrink",
            "answer": "Where the answer is recorded",
        },
        "why": """
            Find the shortest part of `s` that contains every letter of `t`. The loop, the two
            edges and the `while` that moves `left` are the same. Only the highlighted parts change.

            The big flip: for the longest window you shrink while it's invalid and record after.
            For the shortest you shrink while it's still valid and record inside the loop, because
            every valid window is a candidate and you want to squeeze it as small as it goes.
        """,
        "code": '''
            from collections import Counter


            def min_window(s, t):
                need = Counter(t)                    #@state
                missing = len(t)                     #@state
                left = 0
                best = ""
                for right in range(len(s)):
                    if need[s[right]] > 0:           #@state
                        missing -= 1                 #@state
                    need[s[right]] -= 1              #@state
                    while missing == 0:              #@valid
                        if not best or right - left + 1 < len(best):    #@answer
                            best = s[left:right + 1]                     #@answer
                        need[s[left]] += 1           #@state
                        if need[s[left]] > 0:        #@state
                            missing += 1             #@state
                        left += 1
                return best


            print(min_window("ADOBECODEBANC", "ABC"))   # BANC
        ''',
        "check": {
            "question": "For a \"shortest window that satisfies X\" problem, where do you record the answer?",
            "options": [
                "After the `while`, like the longest version",
                "Inside the `while`, before each shrink, while the window is still valid",
                "Once, after the `for` loop ends",
            ],
            "answer": 1,
            "explain": "Inside the `while` every window is valid, so record it, then shrink to try a shorter one. By the time the `while` exits, the window is invalid again.",
        },
    },
]
