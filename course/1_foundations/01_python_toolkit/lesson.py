"""
# Python toolkit for DSA

Most problems get much shorter once you know Python's built-in tools.
Learn these once and you'll use them in every topic after this.

## Built-in structures and their costs
- `list` is a dynamic array. Fast: `append`, `pop()`, `a[i]`. Slow, O(n): `insert(0, x)`, `pop(0)`, `x in a`
- `dict` is a hash map: get, set and `in` are O(1)
- `set` gives O(1) membership, plus `a & b`, `a | b`, `a - b`
- `str` is immutable: build strings with `"".join(parts)`, not `s += x` in a loop
- `tuple` is hashable, so it can be a dict key or live in a set: `seen.add((row, col))`

## collections: reach for these first
- `Counter(items)` counts everything in one line; `.most_common(k)` gives the top k
- `defaultdict(list)` means no more `if key not in d: d[key] = []`
- `deque` gives O(1) `append` and `popleft`. It's your queue

## Built-ins you'll use constantly
- `enumerate(a)` for index and value together, `zip(a, b)` to walk two lists at once
- `sorted(a, key=len, reverse=True)`. Sort by several things with a tuple key: `key=lambda p: (p[1], p[0])`
- `min(a, key=...)`, `max(a, key=...)`, `sum`, `any`, `all`
- `float("inf")` as a starting value for "the best so far"
- `divmod(n, 10)` gives `(n // 10, n % 10)`
- Slices copy: `a[::-1]` is reversed, `a[:]` is a shallow copy

## Modules worth knowing
- `heapq`: a min-heap on a plain list
- `bisect`: binary search on a sorted list
- `itertools`: `accumulate`, `combinations`, `permutations`, `product`
- `functools.cache`: memoisation in one line

## Best practices
- Use names that say what they hold: `left, right` beats `i, j`
- Swap without a temporary: `a, b = b, a`
- Never add or remove items in a list while looping over it; build a new list instead

Press Run to see every tool in action, then change the inputs and run again.
"""
from bisect import bisect_left
from collections import Counter, defaultdict, deque
from heapq import heapify, heappop, nlargest
from itertools import accumulate

# Counter: frequencies in one line
votes = ["ann", "bob", "ann", "cy", "ann", "bob"]
counts = Counter(votes)
print("counts:        ", counts)
print("top 2:         ", counts.most_common(2))

# defaultdict: group things without checking for missing keys
by_length = defaultdict(list)
for word in ["hi", "sun", "go", "cat", "moon"]:
    by_length[len(word)].append(word)
print("grouped:       ", dict(by_length))

# deque: a real queue
queue = deque([1, 2, 3])
queue.append(4)
print("popleft:       ", queue.popleft(), "leaves", list(queue))

# sorting with a key: by age, then by name
people = [("zoe", 25), ("adam", 31), ("ben", 25)]
print("sorted:        ", sorted(people, key=lambda p: (p[1], p[0])))
print("longest word:  ", max(["a", "abcd", "ab"], key=len))

# enumerate + zip
for i, (letter, score) in enumerate(zip("abc", [10, 20, 30])):
    print(f"  row {i}: {letter} = {score}")

# heapq: the smallest item, fast
nums = [9, 4, 7, 1, 8]
heapify(nums)
print("smallest:      ", heappop(nums), "   3 largest:", nlargest(3, [9, 4, 7, 1, 8]))

# bisect: where would 6 go in a sorted list?
print("insert 6 at:   ", bisect_left([1, 3, 5, 7, 9], 6))

# accumulate: running totals
print("running sum:   ", list(accumulate([1, 2, 3, 4])))

# join, don't +=
print("joined:        ", "-".join(str(n) for n in range(5)))

# set operations
a, b = {1, 2, 3, 4}, {3, 4, 5}
print("both / either / only a:", a & b, a | b, a - b)

# unpacking, swapping, divmod
x, y = 1, 2
x, y = y, x
first, *rest = [10, 20, 30]
print("swap:", x, y, "  first/rest:", first, rest, "  divmod(47, 10):", divmod(47, 10))
