"""
# Arrays and strings

Arrays (Python lists) and strings are the input to most problems. The skill
here is walking them cleanly and changing them in place without bugs.

## Walking a list
- `for x in a` when you only need values
- `for i, x in enumerate(a)` when you need the index too
- `for i in range(len(a) - 1): a[i], a[i + 1]` to compare neighbours
- `for i in range(len(a) - 1, -1, -1)` or `reversed(a)` to walk backwards

## In-place tricks
- Swap: `a[i], a[j] = a[j], a[i]`
- Reverse a section: `a[i:j] = a[i:j][::-1]`, or two pointers swapping inwards
- Rotate right by k: `a[:] = a[-k:] + a[:-k]` (do `k %= len(a)` first)
- "Write pointer": keep an index `w` for where the next kept item goes. Copy
  good items to `a[w]` and bump `w`. This removes or moves items in O(n)

## Strings
- Strings can't be changed. Convert with `chars = list(s)`, edit, then `"".join(chars)`
- `s.split()`, `" ".join(words)`, `s.strip()`, `s.lower()`
- `c.isalnum()`, `c.isdigit()`, `c.isalpha()`
- `ord(c) - ord("a")` maps a to z onto 0 to 25, handy for a 26-slot count array
- `zip(*words)` walks strings column by column

## Common mistakes
- Off-by-one: the last index is `len(a) - 1`
- `a[-1]` on an empty list raises IndexError. Check `if a:` first
- `b = a` does not copy. Both names point to the same list. Use `a[:]` or `list(a)`
- `[[0] * cols] * rows` makes rows that are the same list. Use
  `[[0] * cols for _ in range(rows)]`

Press Run to see these tricks in action.
"""
nums = [0, 1, 0, 3, 12]

# Write pointer: keep the non-zeros in order
write = 0
for x in nums:
    if x != 0:
        nums[write] = x
        write += 1
for i in range(write, len(nums)):
    nums[i] = 0
print("zeros to the end:", nums)

# Rotate right by k with slicing
a = [1, 2, 3, 4, 5, 6, 7]
k = 3 % len(a)
a[:] = a[-k:] + a[:-k]
print("rotated by 3:    ", a)

# Reverse in place with two pointers
chars = list("stressed")
left, right = 0, len(chars) - 1
while left < right:
    chars[left], chars[right] = chars[right], chars[left]
    left += 1
    right -= 1
print("reversed:        ", "".join(chars))

# Column by column with zip(*)
words = ["flower", "flow", "flight"]
for column in zip(*words):
    print("  column:", column, "all same" if len(set(column)) == 1 else "differs")

# Letter counts in a 26-slot array
counts = [0] * 26
for c in "banana":
    counts[ord(c) - ord("a")] += 1
print("a, b, n counts:  ", counts[0], counts[1], counts[13])

# The grid trap
bad = [[0] * 3] * 2
bad[0][0] = 9
good = [[0] * 3 for _ in range(2)]
good[0][0] = 9
print("shared rows:", bad, "  separate rows:", good)
