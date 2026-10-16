"""Where are you starting?

READY: one Python question per skill. Missing two or more suggests learning some Python first.
TOPICS: two questions for every Stage 1-4 topic, the more telling one first ("Done DSA" asks only that one).
A question marked "output": True must print exactly options[answer]: `python server.py --check starting`
runs every one of them.
"""

READY = [
    {
        "skill": "names",
        "question": "What does this print?",
        "code": """
            x = 3
            x = x + 2
            print(x)
        """,
        "options": ["3", "5", "x + 2"],
        "answer": 1,
        "explain": "The second line reads `x` (3), adds 2, and points `x` at the result, 5.",
        "output": True,
    },
    {
        "skill": "loops",
        "question": "What does this print?",
        "code": """
            total = 0
            for i in range(1, 5):
                if i % 2 == 0:
                    total += i
            print(total)
        """,
        "options": ["4", "6", "10", "2"],
        "answer": 1,
        "explain": "`range(1, 5)` gives 1, 2, 3, 4. Only 2 and 4 are even, so `total` ends at 6.",
        "output": True,
    },
    {
        "skill": "functions",
        "question": "What does this print?",
        "code": """
            def double(n):
                n * 2

            print(double(4))
        """,
        "options": ["8", "None", "4"],
        "answer": 1,
        "explain": "The function works out `n * 2` but never returns it, so the call gives `None`.",
        "output": True,
    },
    {
        "skill": "lists",
        "question": "What does this print?",
        "code": """
            nums = [10, 20, 30, 40]
            print(nums[1] + nums[-1])
        """,
        "options": ["30", "50", "60", "70"],
        "answer": 2,
        "explain": "Indexes start at 0, so `nums[1]` is 20, and `nums[-1]` is the last item, 40.",
        "output": True,
    },
    {
        "skill": "dicts",
        "question": "What does this print?",
        "code": """
            counts = {}
            for ch in "banana":
                counts[ch] = counts.get(ch, 0) + 1
            print(counts["a"])
        """,
        "options": ["1", "2", "3", "6"],
        "answer": 2,
        "explain": "`counts.get(ch, 0)` starts each letter at 0, and a appears three times in banana.",
        "output": True,
    },
    {
        "skill": "objects",
        "question": "What does this print?",
        "code": """
            class Node:
                def __init__(self, val):
                    self.val = val
                    self.next = None

            a = Node(1)
            b = Node(2)
            a.next = b
            print(a.next.val)
        """,
        "options": ["1", "2", "None", "an error"],
        "answer": 1,
        "explain": "`a.next` points at the node `b`, and `b.val` is 2.",
        "output": True,
    },
]

TOPICS = {
    "01_big_o_in_practice": [
        {
            "question": "How many times does `work()` run?",
            "code": """
                for i in range(n):
                    for j in range(i):
                        work()
            """,
            "options": ["n", "about n²/2", "n log n", "2n"],
            "answer": 1,
            "explain": "The inner loop runs 0, 1, 2, … n − 1 times: n(n − 1)/2 in all, which grows like n².",
        },
        {
            "question": "The input has up to 200,000 numbers. Which idea is fast enough?",
            "options": ["Compare every pair: O(n²)", "Sort, then one pass: O(n log n)", "Try every subset: O(2ⁿ)"],
            "answer": 1,
            "explain": "200,000² is 40 billion steps, far too many. n log n is a few million.",
        },
    ],
    "02_python_toolkit": [
        {
            "question": "Which line is O(n) on a list `a` of n items?",
            "options": ["`a.append(x)`", "`x in a`", "`a[i]`", "`a.pop()`"],
            "answer": 1,
            "explain": "Membership in a list checks items one by one. `append`, indexing and `pop()` from the end are O(1).",
        },
        {
            "question": "What does this print?",
            "code": """
                from collections import Counter
                print(Counter("hello").most_common(1))
            """,
            "options": ["[('l', 2)]", "[('h', 1)]", "{'l': 2}", "2"],
            "answer": 0,
            "explain": "`Counter` counts each letter, and `most_common(1)` returns the top `(item, count)` pair in a list.",
            "output": True,
        },
    ],
    "03_arrays_and_strings": [
        {
            "question": "What does this print?",
            "code": """
                a = [1, 2, 3, 4, 5]
                k = 2
                print(a[-k:] + a[:-k])
            """,
            "options": ["[4, 5, 1, 2, 3]", "[3, 4, 5, 1, 2]", "[1, 2, 3, 4, 5]"],
            "answer": 0,
            "explain": "`a[-2:]` is the last two items and `a[:-2]` is the rest: the list rotated right by 2.",
            "output": True,
        },
        {
            "question": "An array of length n is rotated right by k. Where does the item at index i end up?",
            "options": ["`(i + k) % n`", "`(i - k) % n`", "`i + k`", "`n - i - k`"],
            "answer": 0,
            "explain": "Every item moves k places right and wraps past the end, so the new index is taken modulo n.",
        },
    ],
    "04_hashing": [
        {
            "question": "In one pass over an unsorted list, you want to know whether any two numbers add up to "
                        "`target`. What do you keep as you go?",
            "options": ["The numbers seen so far, in a set", "The list, sorted", "Every pair's sum", "Only the previous number"],
            "answer": 0,
            "explain": "For each x, check whether `target - x` is already in the set, then add x. Each check is O(1).",
        },
        {
            "question": "What does this print?",
            "code": """
                groups = {}
                for w in ["eat", "tea", "tan"]:
                    key = "".join(sorted(w))
                    groups.setdefault(key, []).append(w)
                print(len(groups))
            """,
            "options": ["1", "2", "3"],
            "answer": 1,
            "explain": "Sorted letters make a key that anagrams share: eat and tea both give aet, while tan gives ant.",
            "output": True,
        },
    ],
    "05_recursion": [
        {
            "question": "What does this print?",
            "code": """
                def f(n):
                    if n == 0:
                        return 0
                    return n + f(n - 1)

                print(f(4))
            """,
            "options": ["4", "10", "24", "an error"],
            "answer": 1,
            "explain": "f(4) = 4 + f(3) = 4 + 3 + 2 + 1 + 0 = 10.",
            "output": True,
        },
        {
            "question": "What happens if you delete the `if n == 0` check from `f`?",
            "options": ["It returns 0", "It calls itself until Python stops it with a RecursionError",
                        "It returns n", "It runs once and stops"],
            "answer": 1,
            "explain": "Without a base case nothing stops the calls. Python gives up after about 1,000 levels.",
        },
    ],
    "06_two_pointers": [
        {
            "question": "Find two numbers in a sorted array that add up to `target`, in O(n) time and O(1) extra "
                        "space. How?",
            "options": ["A pointer at each end: move the left one right if the sum is too small, the right one left if it's too big",
                        "Store every number in a set", "Check every pair", "Sort the array again first"],
            "answer": 0,
            "explain": "The sorted order tells you which pointer to move, and each one only moves inward: one pass, no extra memory.",
        },
        {
            "question": "What does this print?",
            "code": """
                s = "racecar"
                i, j = 0, len(s) - 1
                while i < j and s[i] == s[j]:
                    i += 1
                    j -= 1
                print(i >= j)
            """,
            "options": ["True", "False"],
            "answer": 0,
            "explain": "The pointers meet in the middle without finding a mismatch, so racecar reads the same both ways.",
            "output": True,
        },
    ],
    "07_sliding_window": [
        {
            "question": "Longest substring with no repeated letter: `right` moves forward one letter at a time. "
                        "When does `left` move?",
            "options": ["While the window holds a repeated letter", "Every step", "Never", "Only when `right` reaches the end"],
            "answer": 0,
            "explain": "Shrink from the left until the window is valid again (no repeats), then record its length.",
        },
        {
            "question": "What does this print?",
            "code": """
                nums = [2, 1, 5, 1, 3, 2]
                k = 3
                window = sum(nums[:k])
                best = window
                for i in range(k, len(nums)):
                    window += nums[i] - nums[i - k]
                    best = max(best, window)
                print(best)
            """,
            "options": ["8", "9", "10", "14"],
            "answer": 1,
            "explain": "Each step adds the item coming in and drops the one leaving: the window sums are 8, 7, 9, 6.",
            "output": True,
        },
    ],
    "08_prefix_sums": [
        {
            "question": "What does this print?",
            "code": """
                nums = [3, 1, 4, 1, 5]
                prefix = [0]
                for x in nums:
                    prefix.append(prefix[-1] + x)
                print(prefix[4] - prefix[1])
            """,
            "options": ["6", "5", "9", "10"],
            "answer": 0,
            "explain": "`prefix[i]` is the sum of the first i items, so `prefix[4] - prefix[1]` is 1 + 4 + 1 = 6.",
            "output": True,
        },
        {
            "question": "Count the subarrays that sum to k when the array has negative numbers. What works in O(n)?",
            "options": ["A running sum, plus a dict counting how often each running sum has appeared",
                        "A sliding window", "Sorting first, then two pointers", "Checking every subarray"],
            "answer": 0,
            "explain": "Negative numbers break a window's grow-and-shrink logic. A subarray ending here sums to k exactly "
                       "when `running - k` appeared before.",
        },
    ],
    "09_binary_search": [
        {
            "question": "What does this print?",
            "code": """
                from bisect import bisect_left
                print(bisect_left([1, 3, 5, 7], 6))
            """,
            "options": ["2", "3", "4"],
            "answer": 1,
            "explain": "6 belongs just before 7, which is at index 3.",
            "output": True,
        },
        {
            "question": "Find the smallest eating speed that finishes every pile within h hours. Why can you "
                        "binary search the speed?",
            "options": ["If a speed works, every faster speed works too", "The piles are sorted",
                        "The speeds are small numbers", "Each pile takes one hour"],
            "answer": 0,
            "explain": "The check 'finishes in time' flips from no to yes once as the speed grows, so binary search finds the first yes.",
        },
    ],
    "10_sorting_and_intervals": [
        {
            "question": "What does this print?",
            "code": """
                intervals = [[1, 3], [8, 10], [2, 6]]
                intervals.sort()
                merged = [intervals[0]]
                for start, end in intervals[1:]:
                    if start <= merged[-1][1]:
                        merged[-1][1] = max(merged[-1][1], end)
                    else:
                        merged.append([start, end])
                print(merged)
            """,
            "options": ["[[1, 6], [8, 10]]", "[[1, 3], [2, 6], [8, 10]]", "[[1, 10]]"],
            "answer": 0,
            "explain": "After sorting by start, [2, 6] overlaps [1, 3] and stretches it to [1, 6]. [8, 10] starts after 6.",
            "output": True,
        },
        {
            "question": "What does this print?",
            "code": """
                people = [("ann", 30), ("bob", 25), ("cy", 30)]
                print(sorted(people, key=lambda p: (-p[1], p[0]))[0][0])
            """,
            "options": ["ann", "bob", "cy"],
            "answer": 0,
            "explain": "The key sorts by age, oldest first (`-p[1]`), and breaks ties by name, so ann comes before cy.",
            "output": True,
        },
    ],
    "11_greedy": [
        {
            "question": "Each value is your maximum jump length. To decide whether you can reach the last index, "
                        "what is enough to track?",
            "options": ["The farthest index you can reach so far", "Every path you could take",
                        "The number of jumps made", "The smallest value seen"],
            "answer": 0,
            "explain": "Walk left to right. If i is ever past the farthest reach you're stuck; otherwise update it with i + nums[i].",
        },
        {
            "question": "Coins are 1, 3 and 4, and the amount is 6. Always taking the biggest coin gives 4 + 1 + 1. "
                        "What's the fewest coins possible?",
            "options": ["2", "3", "4"],
            "answer": 0,
            "explain": "3 + 3 uses two coins. Taking the biggest coin first isn't always best; this problem needs DP.",
        },
    ],
    "12_stacks": [
        {
            "question": "What does this print?",
            "code": """
                stack = []
                for ch in "(()":
                    if ch == "(":
                        stack.append(ch)
                    elif stack:
                        stack.pop()
                print(len(stack))
            """,
            "options": ["0", "1", "2"],
            "answer": 1,
            "explain": "Two opening brackets and one closing bracket leave one unmatched `(` on the stack.",
            "output": True,
        },
        {
            "question": "For each day's temperature, find how many days until a warmer one. What gives O(n)?",
            "options": ["A stack of days still waiting for a warmer day", "A queue of every day",
                        "Sorting the temperatures", "A dict from temperature to day"],
            "answer": 0,
            "explain": "Each day is pushed once and popped once, when a warmer day arrives: a monotonic stack.",
        },
    ],
    "13_queues_and_deques": [
        {
            "question": "What does this print?",
            "code": """
                from collections import deque
                q = deque([1, 2, 3])
                q.append(4)
                q.popleft()
                print(q[0])
            """,
            "options": ["1", "2", "4"],
            "answer": 1,
            "explain": "`popleft()` removes the front item, 1, so 2 is now at the front.",
            "output": True,
        },
        {
            "question": "Why use `deque.popleft()` rather than `list.pop(0)` for a queue?",
            "options": ["`popleft()` is O(1); `pop(0)` shifts every remaining item, O(n)", "`pop(0)` removes the last item",
                        "A list can't hold more than 1,000 items", "They take the same time"],
            "answer": 0,
            "explain": "After `pop(0)` a list moves every remaining item one place left. A deque doesn't have to.",
        },
    ],
    "14_linked_lists": [
        {
            "question": "What does this print?",
            "code": """
                class ListNode:
                    def __init__(self, val, next=None):
                        self.val = val
                        self.next = next

                head = ListNode(1, ListNode(2, ListNode(3)))
                prev, node = None, head
                while node:
                    nxt = node.next
                    node.next = prev
                    prev = node
                    node = nxt
                print(prev.val)
            """,
            "options": ["1", "3", "None"],
            "answer": 1,
            "explain": "The loop reverses the links one node at a time. At the end `prev` is the old tail, 3: the new head.",
            "output": True,
        },
        {
            "question": "How do you find the middle node of a linked list in one pass?",
            "options": ["Move one pointer one step and another two steps at a time; when the fast one reaches the end, the slow one is in the middle",
                        "Binary search on the nodes", "Reverse it, then walk to the middle", "Jump straight to index n // 2"],
            "answer": 0,
            "explain": "Fast and slow pointers: the slow one has always gone half as far as the fast one.",
        },
    ],
    "15_trees": [
        {
            "question": "What does this print?",
            "code": """
                class TreeNode:
                    def __init__(self, val, left=None, right=None):
                        self.val, self.left, self.right = val, left, right

                def depth(node):
                    if node is None:
                        return 0
                    return 1 + max(depth(node.left), depth(node.right))

                root = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
                print(depth(root))
            """,
            "options": ["2", "3", "4"],
            "answer": 1,
            "explain": "The longest path from the root is 1 → 2 → 4: three nodes.",
            "output": True,
        },
        {
            "question": "Which traversal visits a tree level by level?",
            "options": ["Breadth-first, with a queue", "Pre-order recursion", "In-order recursion", "Post-order recursion"],
            "answer": 0,
            "explain": "A queue hands out every node at depth d before any node at depth d + 1.",
        },
    ],
    "16_binary_search_trees": [
        {
            "question": "What does an in-order traversal of a binary search tree give you?",
            "options": ["The values in sorted order", "The values level by level",
                        "The values in the order they were inserted", "Only the leaves"],
            "answer": 0,
            "explain": "Left subtree < node < right subtree, so visiting left, node, right goes through the values in increasing order.",
        },
        {
            "question": "What does this print?",
            "code": """
                class Node:
                    def __init__(self, val):
                        self.val, self.left, self.right = val, None, None

                def insert(node, val):
                    if node is None:
                        return Node(val)
                    if val < node.val:
                        node.left = insert(node.left, val)
                    else:
                        node.right = insert(node.right, val)
                    return node

                root = None
                for v in [5, 3, 8, 1]:
                    root = insert(root, v)
                print(root.left.left.val)
            """,
            "options": ["1", "3", "8"],
            "answer": 0,
            "explain": "1 is smaller than 5 and then smaller than 3, so it becomes 3's left child.",
            "output": True,
        },
    ],
    "17_heaps": [
        {
            "question": "What does this print?",
            "code": """
                import heapq
                h = [5, 1, 8, 3]
                heapq.heapify(h)
                heapq.heappush(h, 0)
                print(heapq.heappop(h), heapq.heappop(h))
            """,
            "options": ["0 1", "8 5", "5 1", "0 3"],
            "answer": 0,
            "explain": "`heapq` is a min-heap: each pop returns the smallest item left.",
            "output": True,
        },
        {
            "question": "You keep the k largest of n numbers with a min-heap of size k. What does it cost?",
            "options": ["O(n log k)", "O(n²)", "O(k²)", "O(n)"],
            "answer": 0,
            "explain": "Each number costs at most one push and one pop on a heap of size k, which is O(log k).",
        },
    ],
    "18_tries": [
        {
            "question": "Why use a trie for autocomplete instead of a list of words?",
            "options": ["Words that share a prefix share a path, so every word with a prefix sits under one node",
                        "It always uses less memory than a list", "It keeps words in the order they were added",
                        "It finds any word in O(1), however long"],
            "answer": 0,
            "explain": "Walk the prefix's letters once; everything below that node starts with the prefix.",
        },
        {
            "question": "What does this print?",
            "code": """
                trie = {}
                for word in ["car", "cat", "dog"]:
                    node = trie
                    for ch in word:
                        node = node.setdefault(ch, {})
                print(len(trie), len(trie["c"]["a"]))
            """,
            "options": ["2 2", "3 2", "2 1", "3 3"],
            "answer": 0,
            "explain": "car and cat share c → a, then split into r and t. dog starts its own branch, so the root has two children.",
            "output": True,
        },
    ],
    "19_graph_traversal": [
        {
            "question": "Find the fewest moves from start to target on a grid where every move costs the same. "
                        "Which search?",
            "options": ["Breadth-first search (BFS)", "Depth-first search (DFS)", "Trying every path", "Sorting the cells first"],
            "answer": 0,
            "explain": "BFS explores in rings of distance 1, 2, 3 and so on, so it first reaches the target along a shortest path.",
        },
        {
            "question": "What does this print?",
            "code": """
                grid = ["11000",
                        "11000",
                        "00100",
                        "00011"]
                seen = set()

                def flood(r, c):
                    if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
                        return
                    if grid[r][c] == "0" or (r, c) in seen:
                        return
                    seen.add((r, c))
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        flood(r + dr, c + dc)

                islands = 0
                for r in range(len(grid)):
                    for c in range(len(grid[0])):
                        if grid[r][c] == "1" and (r, c) not in seen:
                            flood(r, c)
                            islands += 1
                print(islands)
            """,
            "options": ["2", "3", "4", "5"],
            "answer": 1,
            "explain": "Each flood marks one whole island: the 2×2 block, the single cell, and the pair at the bottom right. "
                       "Diagonals don't connect.",
            "output": True,
        },
    ],
    "20_topological_sort_and_union_find": [
        {
            "question": "Courses have prerequisites. How do you tell whether every course can be finished?",
            "options": ["Look for a cycle in the prerequisite graph, for example with a topological sort",
                        "Sort the courses by number", "Count the courses", "Take the course with the most prerequisites first"],
            "answer": 0,
            "explain": "A cycle means some course depends on itself. A topological sort can order every course only if there's no cycle.",
        },
        {
            "question": "What does this print?",
            "code": """
                parent = list(range(5))

                def find(x):
                    while parent[x] != x:
                        x = parent[x]
                    return x

                def union(a, b):
                    parent[find(a)] = find(b)

                union(0, 1)
                union(3, 4)
                union(1, 4)
                print(find(0) == find(3), find(2) == find(0))
            """,
            "options": ["True False", "False False", "True True", "False True"],
            "answer": 0,
            "explain": "0 joins 1, 3 joins 4, then 1 joins 4, so 0 and 3 end up in one group. 2 never joins anything.",
            "output": True,
        },
    ],
    "21_weighted_graphs": [
        {
            "question": "Find the shortest travel time when roads take different (positive) amounts of time. "
                        "What do you use?",
            "options": ["Dijkstra's algorithm with a min-heap", "Plain BFS", "DFS", "Union-find"],
            "answer": 0,
            "explain": "BFS counts roads, not time. Dijkstra always settles the closest unfinished place next.",
        },
        {
            "question": "What does this print?",
            "code": """
                import heapq
                graph = {"a": [("b", 4), ("c", 1)], "c": [("b", 2)], "b": []}
                dist = {"a": 0}
                heap = [(0, "a")]
                while heap:
                    d, node = heapq.heappop(heap)
                    if d > dist[node]:
                        continue
                    for nxt, w in graph[node]:
                        if d + w < dist.get(nxt, float("inf")):
                            dist[nxt] = d + w
                            heapq.heappush(heap, (d + w, nxt))
                print(dist["b"])
            """,
            "options": ["3", "4", "6"],
            "answer": 0,
            "explain": "Going a → c → b costs 1 + 2 = 3, less than the direct road of 4.",
            "output": True,
        },
    ],
    "22_backtracking": [
        {
            "question": "What does this print?",
            "code": """
                out = []

                def build(path, rest):
                    if not rest:
                        out.append(path)
                        return
                    for i in range(len(rest)):
                        build(path + rest[i], rest[:i] + rest[i + 1:])

                build("", "abc")
                print(len(out))
            """,
            "options": ["3", "6", "8", "9"],
            "answer": 1,
            "explain": "3 choices for the first letter, 2 for the second and 1 for the last: 3 × 2 × 1 = 6 orderings.",
            "output": True,
        },
        {
            "question": "How many subsets does a set of n distinct numbers have?",
            "options": ["2ⁿ", "n²", "n!", "n"],
            "answer": 0,
            "explain": "Each number is either in or out: two choices, made n times.",
        },
    ],
    "23_dynamic_programming_1d": [
        {
            "question": "What does this print?",
            "code": """
                from functools import cache

                @cache
                def ways(n):
                    if n <= 1:
                        return 1
                    return ways(n - 1) + ways(n - 2)

                print(ways(5))
            """,
            "options": ["5", "8", "13", "10"],
            "answer": 1,
            "explain": "The last step was 1 or 2 stairs, so ways(n) = ways(n − 1) + ways(n − 2): 1, 1, 2, 3, 5, 8.",
            "output": True,
        },
        {
            "question": "Adding `@cache` to a recursive function like `ways` changes its running time from…",
            "options": ["O(2ⁿ) to O(n)", "O(n) to O(1)", "O(n²) to O(n log n)", "Nothing; it only saves memory"],
            "answer": 0,
            "explain": "Without memoisation the same subproblems are recomputed exponentially often. With it, each `ways(k)` is worked out once.",
        },
    ],
    "24_dynamic_programming_2d": [
        {
            "question": "What does this print?",
            "code": """
                m, n = 3, 3
                paths = [[1] * n for _ in range(m)]
                for r in range(1, m):
                    for c in range(1, n):
                        paths[r][c] = paths[r - 1][c] + paths[r][c - 1]
                print(paths[m - 1][n - 1])
            """,
            "options": ["4", "6", "9"],
            "answer": 1,
            "explain": "Paths to a cell = paths from above + paths from the left. The bottom-right corner of a 3×3 grid gets 6.",
            "output": True,
        },
        {
            "question": "For the longest common subsequence of strings a and b, what does `dp[i][j]` usually stand for?",
            "options": ["The answer for the first i letters of a and the first j letters of b", "Whether `a[i]` equals `b[j]`",
                        "How many letters a and b have in common anywhere", "Where `a[i]` appears in b"],
            "answer": 0,
            "explain": "Subproblems on prefixes let each cell build on `dp[i-1][j-1]`, `dp[i-1][j]` and `dp[i][j-1]`.",
        },
    ],
    "25_bit_tricks": [
        {
            "question": "What does this print?",
            "code": """
                nums = [4, 1, 2, 1, 2]
                x = 0
                for v in nums:
                    x ^= v
                print(x)
            """,
            "options": ["0", "4", "10", "1"],
            "answer": 1,
            "explain": "XOR cancels pairs (a ^ a is 0), leaving the number that appears once.",
            "output": True,
        },
        {
            "question": "What does this print?",
            "code": """
                print(bin(12), 12 & (12 - 1))
            """,
            "options": ["0b1100 8", "0b1100 11", "0b1010 8", "0b1100 4"],
            "answer": 0,
            "explain": "`n & (n - 1)` clears the lowest set bit: 1100 becomes 1000, which is 8.",
            "output": True,
        },
    ],
}
