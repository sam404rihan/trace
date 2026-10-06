"""
Count grid paths                                                             [guided]

A robot starts in the top-left cell of a grid with `rows` rows and `cols`
columns. It can only move right or down. How many different paths reach the
bottom-right cell?

Example:
    count_paths(2, 3)  ->  3      RRD, RDR, DRR

You'll write the natural recursion first, see it fall over on a bigger grid,
and then fix it with one line of memoisation.
"""


def count_paths(rows: int, cols: int) -> int:
    raise NotImplementedError  # replace this line with your solution


STEPS = [
    {
        "title": "Recurse",
        "text": "The last move into the corner came either from above or from the left. "
                "So paths(r, c) = paths(r - 1, c) + paths(r, c - 1). What's the base case?",
        "hint": "A grid with a single row or a single column has exactly one path: if rows == 1 or cols == 1: return 1.",
        "tests": [
            ((2, 3), 3),
            ((3, 3), 6),
            ((3, 7), 28),
        ],
    },
    {
        "title": "Edges",
        "text": "Thin grids: one row, one column, a single cell.",
        "hint": "Your base case should already cover these. 1 × 1 is one path (do nothing).",
        "tests": [
            ((1, 1), 1),
            ((1, 9), 1),
            ((9, 1), 1),
        ],
    },
    {
        "title": "Remember answers",
        "text": "count_paths(17, 17) makes hundreds of millions of calls, because the same (r, c) is asked for "
                "over and over. Cache each answer the first time you compute it.",
        "hint": "Put @functools.lru_cache(maxsize=None) (or @cache) above the function, or keep a dict memo "
                "of (r, c) -> answer. Then there are only rows × cols different calls.",
        "tests": [
            ((10, 10), 48620),
            ((17, 17), 601080390),
            ((60, 40), 3332420398982499757882998720),
        ],
    },
]
