"""
Course Schedule                                                    [medium] · graphs

There are `num_courses` courses labelled 0 .. num_courses - 1. Each pair
[a, b] in `prerequisites` means you must take course b before course a.
Return True if it's possible to finish every course.

Example:
    course_schedule(2, [[1, 0]])            ->  True    take 0, then 1
    course_schedule(2, [[1, 0], [0, 1]])    ->  False   each needs the other first

Aim for:  O(V + E) time
Hint:     Courses are nodes, prerequisites are edges. You can finish everything
          exactly when the graph has no cycle. Two classic ways to check:
          Kahn's algorithm (repeatedly take courses with no remaining prereqs),
          or DFS with three colours (unvisited / in progress / done).
          structures/graph.py has a topological sort to compare with.
"""


def course_schedule(num_courses: int, prerequisites: list[list[int]]) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((2, [[1, 0]]), True),
    ((2, [[1, 0], [0, 1]]), False),
    ((3, []), True),
    ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False),
    ((5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]), True),
    ((1, [[0, 0]]), False),
]
