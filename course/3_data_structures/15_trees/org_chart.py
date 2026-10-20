"""
Org chart                                                                     [build]

You get (manager, employee) pairs from an HR export. Exactly one person has
no manager: the CEO. Print the org chart:

    org_chart([("Ada", "Bo"), ("Ada", "Cy"), ("Bo", "Di")])
    ->  ["Ada (3)",
         "  Bo (1)",
         "    Di",
         "  Cy"]

Rules:
  - Each line is a name, indented 2 spaces per level below the CEO.
  - Anyone with reports shows "(n)": the number of people under them at any depth.
  - Anyone without reports shows just their name.
  - Reports of the same manager are listed alphabetically.

Hint:     Build a dict manager -> list of reports, and find the CEO as the one manager who
          is never an employee. Then a recursive helper returns (lines, size) for a person,
          just like a tree's height or size.
"""


def org_chart(pairs: list[tuple[str, str]]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


USES = ["hash.group_key", "tree.recursion"]

TESTS = [
    (([("Ada", "Bo"), ("Ada", "Cy"), ("Bo", "Di")],), ["Ada (3)", "  Bo (1)", "    Di", "  Cy"]),
    (([("Zoe", "Amy")],), ["Zoe (1)", "  Amy"]),
    (([("M", "z"), ("M", "a"), ("a", "b"), ("a", "c"), ("c", "d")],),
     ["M (5)", "  a (3)", "    b", "    c (1)", "      d", "  z"]),
    (([("Lead", "Dev1"), ("CEO", "Lead"), ("Lead", "Dev2"), ("CEO", "Ops")],),
     ["CEO (4)", "  Lead (2)", "    Dev1", "    Dev2", "  Ops"]),
]
