"""
# Hashing

A dict or set turns "search the whole list" (O(n)) into "look it up" (O(1)).
It's the most common way to turn an O(n²) idea into O(n).

## Use it when
- You ask "have I seen this before?" (a set)
- You need the index or count of something you've seen (a dict)
- You need to group things that share a property (a dict of lists)
- The problem says "pair", "duplicate", "frequency", "anagram", or "unique"

## The patterns
- **Seen set:** `if x in seen: ...` then `seen.add(x)`
- **Complement lookup:** for each x, look up `target - x` in a dict of value to index
- **Counting:** `Counter(items)`, or `counts[x] = counts.get(x, 0) + 1`
- **Grouping by key:** `groups[key(x)].append(x)` with `defaultdict(list)`.
  The trick is choosing the key: sorted letters, a tuple of counts, `(row, col)`

## Python shortcuts
- `Counter(a) == Counter(b)` checks "same items, same counts"
- `len(set(a)) < len(a)` checks for duplicates
- `counts.most_common(k)` gives the top k
- Keys must be hashable: use tuples, not lists, e.g. `tuple(sorted(word))`

## Common mistakes
- Looking up `d[key]` when the key might be missing raises KeyError. Use `d.get(key, 0)`
- Adding x to the dict before checking for its partner, so x pairs with itself
- Using a list as a key: `TypeError: unhashable type: 'list'`

Press Run to see each pattern.
"""
from collections import Counter, defaultdict

# Seen set: first repeated value
seen = set()
for x in [3, 1, 4, 1, 5]:
    if x in seen:
        print("first repeat:", x)
        break
    seen.add(x)

# Complement lookup: two numbers that add to 10
index_of = {}
for i, x in enumerate([2, 7, 4, 6]):
    if 10 - x in index_of:
        print("pair adding to 10 at indices", index_of[10 - x], i)
    index_of[x] = i

# Counting
print("letter counts:", Counter("mississippi"))
print("same letters? ", Counter("listen") == Counter("silent"))

# Grouping by a computed key
groups = defaultdict(list)
for word in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    groups["".join(sorted(word))].append(word)
print("anagram groups:", list(groups.values()))

# Tuples as keys: count points on the same spot
points = [(1, 2), (3, 4), (1, 2)]
print("point counts: ", Counter(points))
