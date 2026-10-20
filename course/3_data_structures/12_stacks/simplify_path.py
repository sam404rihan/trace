"""
Simplify a file path                                                         [guided]

Given an absolute Unix path, return its simplest form:

  - "." means the current folder (drop it)
  - ".." means go up one folder (if you can)
  - repeated slashes count as one
  - the result starts with "/" and never ends with "/" (except the root itself)

Example:
    simplify_path("/home/user/../docs/./notes/")  ->  "/home/docs/notes"

A stack of folder names is the natural model: a name goes on, ".." comes off.
"""


def simplify_path(path: str) -> str:
    raise NotImplementedError  # replace this line with your solution


USES = ["stack.lifo"]

STEPS = [
    {
        "title": "Names and ..",
        "text": "Split on \"/\". Push each folder name onto a stack. On \"..\", pop. At the end, join the stack with \"/\" and put \"/\" in front.",
        "hint": "parts = path.split(\"/\"). Then \"/\" + \"/\".join(stack).",
        "tests": [
            (("/a/b/../c",), "/a/c"),
            (("/home/",), "/home"),
            (("/x/y/z/../..",), "/x"),
        ],
    },
    {
        "title": "Dots and double slashes",
        "text": "\".\" and empty pieces (from \"//\" or a trailing \"/\") change nothing. Skip them.",
        "hint": "if part in (\"\", \".\"): continue",
        "tests": [
            (("/a/./b//c/",), "/a/b/c"),
            (("/home/user/../docs/./notes/",), "/home/docs/notes"),
            (("///usr///bin/",), "/usr/bin"),
        ],
    },
    {
        "title": "Edges",
        "text": "\"..\" at the root stays at the root. \"...\" is an ordinary folder name. The root on its own is \"/\".",
        "hint": "Only pop when the stack isn't empty.",
        "tests": [
            (("/../",), "/"),
            (("/",), "/"),
            (("/a/../../b",), "/b"),
            (("/.../a",), "/.../a"),
            (("/a/b/c/../../../..",), "/"),
        ],
    },
]
