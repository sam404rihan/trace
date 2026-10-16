def is_happy(n: int) -> bool:
    def step(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    seen = set()                        # a number we've met before means we're going round a loop
    while n != 1 and n not in seen:
        seen.add(n)
        n = step(n)
    return n == 1

    # No set needed (Linked lists topic): Floyd's fast and slow pointers. Move slow one step and
    # fast two; the number is happy if fast reaches 1, and loops if fast catches up with slow.
