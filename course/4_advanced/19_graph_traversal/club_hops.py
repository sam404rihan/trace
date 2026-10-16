"""
Message through clubs                                                         [easy]

`clubs` is a list of clubs, each a list of people. A message passes from a
person to everyone in a club they belong to, and each club it goes through
counts as one hop. Return the fewest hops for a message from `start` to reach
`target`, or -1 if it can't. If start is target, that's 0 hops.

Example:
    club_hops([["ann", "bo"], ["bo", "cy"], ["cy", "dee"]], "ann", "dee")  ->  3
        ann -> bo (club 0), bo -> cy (club 1), cy -> dee (club 2).

Aim for:  O(total names in all clubs): every club is expanded at most once.
Hint:     Index each person to the clubs they're in: clubs_of = {person: [club indexes]}.
          BFS from start. For a person, look at each of their clubs you haven't used yet,
          mark it used, and queue everyone in it at hops + 1.
"""


def club_hops(clubs: list[list[str]], start: str, target: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["graph.groups"]
USES = ["bfs.shortest", "graph.adjacency"]

TESTS = [
    (([["ann", "bo"], ["bo", "cy"], ["cy", "dee"]], "ann", "dee"), 3),
    (([["ann", "bo", "cy"]], "ann", "cy"), 1),
    (([["ann", "bo"], ["cy", "dee"]], "ann", "dee"), -1),
    (([["ann"]], "ann", "ann"), 0),
    (([["ann", "bo"], ["bo", "cy", "dee"], ["ann", "dee"]], "ann", "dee"), 1),
    (([["eve", "fay"], ["ann", "gus"]], "ann", "zed"), -1),
]
