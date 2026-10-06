"""
Pretty-print a table                                                          [build]

Turn rows of strings into the lines of a text table. The first row is the header.

    format_table([["name", "qty"], ["apple", "3"], ["kiwi", "12"]])
    ->  ["name  | qty",
         "------+----",
         "apple |   3",
         "kiwi  |  12"]

Rules:
  - Each column is as wide as its longest cell (header included).
  - Columns are joined with " | ". The separator line uses "-" for every
    character of each column, joined with "-+-".
  - Cells that are numbers (float(cell) works) are right-aligned. Everything
    else is left-aligned. Header cells are always left-aligned.
  - A row shorter than the header is padded with empty cells.
  - Strip trailing spaces from the end of every line.

Hint:     First pass: compute widths. Second pass: build each line with
          cell.ljust(w) or cell.rjust(w), then " | ".join(...).rstrip().
"""


def format_table(rows: list[list[str]]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([["name", "qty"], ["apple", "3"], ["kiwi", "12"]],),
     ["name  | qty", "------+----", "apple |   3", "kiwi  |  12"]),
    (([["city", "temp", "note"], ["Oslo", "-3.5", "cold"], ["Lima", "19", ""]],),
     ["city | temp | note", "-----+------+-----", "Oslo | -3.5 | cold", "Lima |   19 |"]),
    (([["id", "label"], ["1"]],),
     ["id | label", "---+------", " 1 |"]),
    (([["x"]],), ["x", "-"]),
    (([["k", "v"], ["a", "1e3"], ["bb", "n/a"]],),
     ["k  | v", "---+----", "a  | 1e3", "bb | n/a"]),
]
