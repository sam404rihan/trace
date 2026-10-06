def is_happy(n: int) -> bool:
    def step(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    # Floyd's cycle detection: the sequence either hits 1 or loops, and fast catches slow in a loop.
    slow, fast = n, step(n)
    while fast != 1 and slow != fast:
        slow, fast = step(slow), step(step(fast))
    return fast == 1
