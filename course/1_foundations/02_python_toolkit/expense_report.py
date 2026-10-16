"""
Expense report                                                                [build]

You're given the raw lines of a CSV export: `date,category,amount`, e.g.

    "2024-03-01,food,12.50"

Build a summary dict:

    {
      "total":       sum of all valid amounts, rounded to 2 decimals,
      "by_category": [(category, total), ...] biggest total first,
                     ties alphabetical, totals rounded to 2 decimals,
      "busiest_day": the date with the highest spending (earliest date on a tie),
                     or None if there are no valid lines,
      "skipped":     how many lines were malformed,
    }

Rules:
  - Strip spaces around every field. Categories are case-insensitive: store them lowercase.
  - A header line ("date,category,amount") and blank lines are ignored, and don't count as skipped.
  - A line is malformed if it doesn't have exactly 3 fields or the amount isn't a number.

Example:
    expense_report(["2024-03-01,food,10", "2024-03-01,Travel,5.5", "oops"])
    ->  {"total": 15.5, "by_category": [("food", 10.0), ("travel", 5.5)],
         "busiest_day": "2024-03-01", "skipped": 1}

Hint:     Split each line with .split(","), try float(amount) inside try/except ValueError,
          and keep two dicts: category -> total and date -> total.
"""


def expense_report(lines: list[str]) -> dict:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    ((["2024-03-01,food,10", "2024-03-01,Travel,5.5", "oops"],),
     {"total": 15.5, "by_category": [("food", 10.0), ("travel", 5.5)], "busiest_day": "2024-03-01", "skipped": 1}),
    ((["date,category,amount", "2024-01-02, rent , 800", "2024-01-03,food,20.25", "", "2024-01-03,FOOD,4.75"],),
     {"total": 825.0, "by_category": [("rent", 800.0), ("food", 25.0)], "busiest_day": "2024-01-02", "skipped": 0}),
    ((["2024-05-01,a,1", "2024-05-02,b,1", "2024-05-01,b,x", "2024-05-03,c,1,extra"],),
     {"total": 2.0, "by_category": [("a", 1.0), ("b", 1.0)], "busiest_day": "2024-05-01", "skipped": 2}),
    (([],), {"total": 0, "by_category": [], "busiest_day": None, "skipped": 0}),
    ((["2024-06-02,books,0.1", "2024-06-01,books,0.2", "2024-06-02,books,0.1"],),
     {"total": 0.4, "by_category": [("books", 0.4)], "busiest_day": "2024-06-01", "skipped": 0}),
]
