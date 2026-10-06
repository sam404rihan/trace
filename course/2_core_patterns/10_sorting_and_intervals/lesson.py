"""
# Sorting and intervals

Sorting first often makes the rest of a problem a simple loop. In Python you
almost never write a sort yourself. You write a good **key**.

## Sorting tools
- `a.sort()` sorts in place; `sorted(a)` returns a new list. Both O(n log n) and stable
- `key=` computes what to compare: `sorted(words, key=len)`
- Several criteria: `key=lambda p: (p.score, p.name)`
- Descending on one field only: negate it, `key=lambda p: (-p.score, p.name)`
- Weird comparisons ("which order of two strings is better?"):
  `key=functools.cmp_to_key(compare)` where `compare(a, b)` returns negative, 0 or positive
- Stable means equal items keep their original order, so you can sort in two passes

## Intervals: sort by start, then sweep
Interval problems ("meetings", "merge ranges", "free time") almost always start with
```
intervals.sort(key=lambda iv: iv[0])
```
Now any overlap is with the neighbour you just looked at:
```
merged = []
for start, end in intervals:
    if merged and start <= merged[-1][1]:     # overlaps the last one
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
```

## Two intervals [a, b] and [c, d] overlap when
`a <= d and c <= b`, or `max(a, c) <= min(b, d)`.
Decide whether touching ends (b == c) counts. Read the problem.

## Common mistakes
- Forgetting `max()` when merging: [1, 10] and [2, 3] merge to [1, 10], not [1, 3]
- Sorting by end when you meant start (sorting by END is for "most non-overlapping
  meetings", the greedy topic)
- `list.sort()` returns None. `a = a.sort()` loses your list

Press Run to see custom sorting and merging.
"""
from functools import cmp_to_key

players = [("ana", 90), ("bo", 75), ("cy", 90), ("di", 60)]
print("by score desc, then name:", sorted(players, key=lambda p: (-p[1], p[0])))

words = ["banana", "kiwi", "apple", "fig"]
print("by length, then alphabet:", sorted(words, key=lambda w: (len(w), w)))


def compare(a, b):
    """Put a before b if a+b makes a bigger number than b+a."""
    return -1 if a + b > b + a else (1 if a + b < b + a else 0)


print("biggest number from [3, 30, 34, 5, 9]:",
      "".join(sorted(["3", "30", "34", "5", "9"], key=cmp_to_key(compare))))

intervals = [[8, 10], [1, 3], [2, 6], [15, 18], [17, 20]]
intervals.sort(key=lambda iv: iv[0])
merged = []
for start, end in intervals:
    if merged and start <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
print("merged intervals:", merged)
