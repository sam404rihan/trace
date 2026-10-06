"""
Folder tree with sizes                                                        [build]

A folder is a dict:

    {"name": "docs", "files": {"a.txt": 120, "b.md": 30}, "folders": [ ...more folders... ]}

Return the lines of a tree listing, like the `tree` command, with each
folder's total size (every file inside it, at any depth):

    render_folders({"name": "root", "files": {"x.py": 5},
                    "folders": [{"name": "img", "files": {"a.png": 100}, "folders": []}]})
    ->  ["root/ (105)",
         "  img/ (100)",
         "    a.png (100)",
         "  x.py (5)"]

Rules:
  - Each level is indented by 2 more spaces.
  - Inside a folder, list sub-folders first (sorted by name), then files (sorted by name).
  - Folder lines end in "/ (total)". File lines are "name (size)".

Hint:     Write a helper that returns (lines, total) for one folder. It calls itself
          for each sub-folder, adds their totals to its own, and indents their lines.
"""


def render_folders(folder: dict) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


_PROJECT = {
    "name": "project", "files": {"README.md": 4, "setup.py": 2},
    "folders": [
        {"name": "src", "files": {"main.py": 10, "util.py": 6},
         "folders": [{"name": "core", "files": {"engine.py": 20}, "folders": []}]},
        {"name": "assets", "files": {}, "folders": [{"name": "empty", "files": {}, "folders": []}]},
    ],
}

TESTS = [
    (({"name": "root", "files": {"x.py": 5}, "folders": [{"name": "img", "files": {"a.png": 100}, "folders": []}]},),
     ["root/ (105)", "  img/ (100)", "    a.png (100)", "  x.py (5)"]),
    (({"name": "e", "files": {}, "folders": []},), ["e/ (0)"]),
    ((_PROJECT,), [
        "project/ (42)",
        "  assets/ (0)",
        "    empty/ (0)",
        "  src/ (36)",
        "    core/ (20)",
        "      engine.py (20)",
        "    main.py (10)",
        "    util.py (6)",
        "  README.md (4)",
        "  setup.py (2)",
    ]),
    (({"name": "z", "files": {"b": 1, "a": 2}, "folders": [{"name": "y", "files": {"c": 3}, "folders": []},
                                                             {"name": "x", "files": {}, "folders": []}]},),
     ["z/ (6)", "  x/ (0)", "  y/ (3)", "    c (3)", "  a (2)", "  b (1)"]),
]
