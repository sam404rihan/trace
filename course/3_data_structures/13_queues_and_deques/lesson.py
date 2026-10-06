"""
# Queues and deques

First in, first out. Use `collections.deque`: `append` adds to the back,
`popleft` takes from the front, both O(1). A deque is double-ended, so
`appendleft` and `pop` work too.

## Use it when
- Things are handled in arrival order: tasks, requests, BFS levels
- Breadth-first search: always a queue (graphs topic)
- "Last k items" or "recent calls": `deque(maxlen=k)` drops old items automatically
- **Sliding window maximum/minimum**: use a monotonic deque (below)

## Python shortcuts
- `deque(maxlen=3)` keeps only the newest 3 items
- `q.rotate(1)` rotates right by one
- Never use `list.pop(0)` as a queue. It's O(n), so a loop becomes O(n²)

## Pattern: monotonic deque (window max)
Keep indexes whose values are decreasing from front to back:
```
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:   # smaller items can never be the max again
        dq.pop()
    dq.append(i)
    if dq[0] <= i - k:             # front slid out of the window
        dq.popleft()
    if i >= k - 1:
        result.append(a[dq[0]])    # front is always the window's max
```

## Common mistakes
- Checking `if q:` on a deque works; checking `len(q) == 0` works too. Pick one
- Forgetting to evict the front when it leaves the window
- Using a heap for window max. It works, but lazy deletion is fiddly and the deque is O(n)

Press Run to see a queue, a bounded deque, and the window max.
"""
from collections import deque

queue = deque()
for customer in ["ana", "bo", "cy"]:
    queue.append(customer)
while queue:
    print("serving", queue.popleft(), "| still waiting:", list(queue))

recent = deque(maxlen=3)
for page in ["home", "about", "blog", "contact", "shop"]:
    recent.append(page)
print("last 3 pages:", list(recent))


def window_max(nums, k):
    dq, result = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


print("window max, k=3:", window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
