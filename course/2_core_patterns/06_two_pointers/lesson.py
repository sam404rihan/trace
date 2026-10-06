"""
# Two pointers

Two indexes move through the data instead of a nested loop. That's O(n)
instead of O(n²).

## Use it when
- The input is sorted (or you're allowed to sort it) and you want a pair
- You compare things from both ends: palindromes, reversing, "container"
- You filter or compact a list in place (a slow "write" pointer and a fast "read" pointer)

## Pattern 1: opposite ends
```
left, right = 0, len(a) - 1
while left < right:
    if good(a[left], a[right]):
        ...                      # record the answer
    if need_bigger:
        left += 1
    else:
        right -= 1
```
Each step throws away one element for good, so it's O(n).

## Pattern 2: same direction (slow and fast)
```
slow = 0
for fast in range(len(a)):
    if keep(a[fast]):
        a[slow] = a[fast]
        slow += 1
```

## Python shortcuts
- `a.sort()` first. O(n log n) is almost always acceptable
- Skip duplicates: `while left < right and a[left] == a[left - 1]: left += 1`
- `s == s[::-1]` checks a palindrome in one line when you don't need O(1) space

## Common mistakes
- `while left <= right` when a pair needs two different elements
- Forgetting to move a pointer in some branch: infinite loop
- Sorting when the problem wants original indexes. Store `(value, index)` pairs first

## Spot it
"sorted array", "pair that sums to", "palindrome", "in place", "remove duplicates"

Press Run to see both patterns.
"""


def pair_with_sum(nums, target):
    """Opposite ends on a sorted list."""
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        print(f"  left={left} right={right}  {nums[left]} + {nums[right]} = {total}")
        if total == target:
            return left, right
        if total < target:
            left += 1        # need a bigger sum: move the small end up
        else:
            right -= 1       # need a smaller sum: move the big end down
    return None


print("pair summing to 13:", pair_with_sum([1, 3, 4, 6, 9, 11], 13))


def remove_value(nums, value):
    """Same direction: slow marks where the next kept item goes."""
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != value:
            nums[slow] = nums[fast]
            slow += 1
    return nums[:slow]


print("without 3s:", remove_value([3, 2, 2, 3, 4, 3], 3))


def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left, right = left + 1, right - 1
    return True


print("racecar:", is_palindrome("racecar"), "  python:", is_palindrome("python"))
