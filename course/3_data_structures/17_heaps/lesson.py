"""
# Heaps (priority queues)

A heap always gives you the smallest item in O(1) and removes it in O(log n).
Python's `heapq` turns a plain list into a min-heap.

## Use it when
- "k largest", "k smallest", "k closest", "top k"
- You repeatedly need the current smallest/largest while items keep arriving
- Merging several sorted lists
- Scheduling: always run the task with the earliest time or highest priority
- Dijkstra's shortest path (advanced stage)

## heapq cheat sheet
- `heapify(a)`: turn a list into a heap in place, O(n)
- `heappush(h, x)` / `heappop(h)`: O(log n)
- `h[0]`: peek at the smallest, O(1)
- `heappushpop(h, x)`: push then pop, faster than doing both
- `nlargest(k, items, key=...)`, `nsmallest(k, items, key=...)`

## Tricks
- **Max-heap:** push `-x`, and negate again when you pop
- **Priorities with data:** push tuples `(priority, item)`. Ties compare the next
  field, so add a counter if items can't be compared: `(priority, count, item)`
- **Top k largest with a size-k MIN-heap:** push each item, pop when the size
  passes k. What's left is the k largest, and `h[0]` is the k-th largest.
  That's O(n log k) and O(k) memory

## Common mistakes
- Expecting `heapq` to be a max-heap. It's always min
- Thinking the list is sorted. Only `h[0]` is guaranteed; the rest is heap order
- Pushing objects that can't be compared, e.g. two ListNodes with equal priority:
  `TypeError`. Use the counter trick

Press Run to see a heap in action.
"""
import heapq

h = []
for x in [5, 1, 8, 3, 9, 2]:
    heapq.heappush(h, x)
print("heap list (not sorted!):", h, " smallest:", h[0])
print("pop in order:", [heapq.heappop(h) for _ in range(len(h))])

# Max-heap via negation
max_heap = [-x for x in [5, 1, 8, 3]]
heapq.heapify(max_heap)
print("largest:", -heapq.heappop(max_heap))

# k largest with a size-k min-heap
nums, k = [7, 10, 4, 3, 20, 15], 3
top = []
for x in nums:
    heapq.heappush(top, x)
    if len(top) > k:
        heapq.heappop(top)       # drop the smallest of the candidates
print(f"{k} largest:", sorted(top), f" {k}rd largest:", top[0])

# Tasks by priority, with a counter to break ties
tasks = []
for count, (priority, name) in enumerate([(2, "email"), (1, "fix prod bug"), (2, "lunch"), (3, "tidy desk")]):
    heapq.heappush(tasks, (priority, count, name))
while tasks:
    priority, _, name = heapq.heappop(tasks)
    print(f"  priority {priority}: {name}")

print("3 closest to 0:", heapq.nsmallest(3, [-7, 2, -1, 9, 4], key=abs))
