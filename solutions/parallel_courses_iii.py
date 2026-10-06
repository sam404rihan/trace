def parallel_courses_iii(n: int, relations: list[list[int]], time: list[int]) -> int:
    unlocks = [[] for _ in range(n)]
    waiting = [0] * n                   # unfinished prerequisites per course
    for a, b in relations:
        unlocks[a].append(b)
        waiting[b] += 1
    start = [0] * n                     # earliest month each course can start
    ready = deque(i for i in range(n) if waiting[i] == 0)
    total = 0
    while ready:                        # Kahn's algorithm: prerequisites always come first
        course = ready.popleft()
        done = start[course] + time[course]
        total = max(total, done)
        for nxt in unlocks[course]:
            start[nxt] = max(start[nxt], done)
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                ready.append(nxt)
    return total
