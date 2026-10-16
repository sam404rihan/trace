"""
Key, door, exit                                                               [easy]

The grid is a list of strings:
    "@"   your start          "E"   the exit
    "."   open floor          "#"   wall
    "k"   a key               "D"   a door: you can walk through it only once you hold the key
Each step moves up, down, left or right. Return the fewest steps to reach the
exit, or -1 if you can't.

Example:
    key_then_exit(["@D.E",
                   "k#.#"])  ->  5
        Down to the key, back up, through the door, then two more steps.

Aim for:  O(rows * cols).
Hint:     A plain BFS on cells breaks: you may need to walk back over a cell after picking up
          the key. So the BFS state is (row, col, has_key), and `seen` holds states, not
          cells. Stepping onto the key sets has_key to True.
"""


def key_then_exit(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.state"]
USES = ["bfs.shortest", "grid.neighbors"]

TESTS = [
    ((["@.E"],), 2),
    ((["@D.E", "k#.#"],), 5),
    ((["@.#E", "k.D."],), 5),
    ((["@#E", "k#."],), -1),
    ((["@...", "##D#", "k..E"],), -1),
    ((["@k", "DE"],), 2),
]
