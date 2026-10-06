from collections import deque


def course_schedule(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # Kahn's algorithm (topological sort by BFS). O(V + E).
    # Repeatedly take any course with no remaining prerequisites. If a cycle
    # exists, the courses in it never reach zero and we can't take them all.
    unlocks = [[] for _ in range(num_courses)]
    missing = [0] * num_courses                # prerequisites not yet taken
    for course, needed in prerequisites:
        unlocks[needed].append(course)
        missing[course] += 1

    ready = deque(c for c in range(num_courses) if missing[c] == 0)
    taken = 0
    while ready:
        course = ready.popleft()
        taken += 1
        for nxt in unlocks[course]:
            missing[nxt] -= 1
            if missing[nxt] == 0:
                ready.append(nxt)
    return taken == num_courses
