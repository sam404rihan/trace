"""
# Stacks

Last in, first out. In Python a stack is just a list: `append` to push,
`pop()` to pop, `stack[-1]` to peek. All O(1).

## Use it when
- Things must be closed in reverse order of opening: brackets, tags, undo
- You process something and later need "the most recent unfinished one"
- Expressions: calculators, Reverse Polish Notation
- **"Next greater / next smaller element"**: use a monotonic stack (below)
- You want DFS without recursion

## Pattern: matching pairs
```
pairs = {")": "(", "]": "["}
for ch in s:
    if ch in pairs:
        if not stack or stack.pop() != pairs[ch]: return False
    else:
        stack.append(ch)
return not stack
```

## Pattern: monotonic stack
Keep the stack sorted (e.g. decreasing). Before pushing a new item, pop
everything it "beats". Each popped item has just found its next greater element.
```
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        j = stack.pop()
        answer[j] = i          # x is the next greater element for j
    stack.append(i)            # store INDEXES, not values
```
Every index is pushed once and popped once, so it's O(n) even with the inner while.

## Common mistakes
- `stack.pop()` or `stack[-1]` on an empty stack. Check `if stack` first
- Forgetting leftovers: items still on the stack at the end are "unclosed" or "no answer"
- Storing values when you need distances. Store indexes

Press Run to see a monotonic stack at work.
"""


def next_greater(nums):
    answer = [-1] * len(nums)
    stack = []                              # indexes still waiting for something bigger
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            answer[j] = x
            print(f"  {x} is the next greater element for {nums[j]}")
        stack.append(i)
    return answer


print("next greater:", next_greater([2, 1, 5, 3, 4, 6]))


def undo_demo():
    text, history = "", []
    for action in ["type:Hello", "type: world", "undo", "type: there"]:
        if action == "undo":
            text = history.pop()
        else:
            history.append(text)
            text += action.split(":", 1)[1]
        print(f"  {action:<13} -> {text!r}")


undo_demo()
