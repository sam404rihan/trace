"""
# Backtracking

Build an answer one choice at a time. When a partial answer can't work, undo
the last choice and try the next one. It's a DFS over decisions.

## Use it when
- "Return ALL" combinations, subsets, permutations, arrangements, paths
- Puzzles with constraints: N-queens, sudoku, word search
- Inputs are small (n ≤ 20 or so), because the answer count itself explodes

## The template
```
result, path = [], []

def explore(start):
    if is_complete(path):
        result.append(path[:])        # COPY: path keeps changing
        return
    for choice in choices_from(start):
        if not allowed(choice):
            continue                  # prune early: this is what makes it fast
        path.append(choice)           # choose
        explore(next_start)           # explore
        path.pop()                    # un-choose
```

## The three shapes
- **Subsets / combinations:** loop `i` from `start`, recurse with `i + 1`,
  so you never go backwards and never repeat a set
- **Reuse allowed** (combination sum): recurse with `i`, not `i + 1`
- **Permutations:** loop over everything, skipping items already `used`

## Pruning tips
- Sort first, then `break` as soon as a choice is too big
- Skip duplicates: `if i > start and nums[i] == nums[i - 1]: continue`
- Track what's used in sets (columns, diagonals) for O(1) checks

## Common mistakes
- `result.append(path)` without copying: every answer ends up as the same empty list
- Forgetting to undo (`pop`), which leaks choices into other branches
- Generating everything and filtering at the end, when you could prune early

Press Run to see the choose / explore / un-choose rhythm.
"""


def subsets_verbose(nums):
    result, path = [], []

    def explore(start, depth):
        result.append(path[:])
        print("  " * depth + str(path))
        for i in range(start, len(nums)):
            path.append(nums[i])          # choose
            explore(i + 1, depth + 1)     # explore
            path.pop()                    # un-choose

    explore(0, 0)
    return result


print("every subset of [1, 2, 3], as the search visits them:")
subsets_verbose([1, 2, 3])


def combos_to_target(candidates, target):
    candidates = sorted(candidates)
    result, path = [], []

    def explore(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                     # sorted: everything after is too big as well
            path.append(candidates[i])
            explore(i + 1, remaining - candidates[i])
            path.pop()

    explore(0, target)
    return result


print("\ndifferent numbers from [2, 3, 5, 6, 8] adding to 8:", combos_to_target([2, 3, 5, 6, 8], 8))
