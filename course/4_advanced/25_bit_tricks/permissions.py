"""
User permissions as bit flags                                                 [build]

Store every user's permissions in ONE integer, one bit per permission, the way
operating systems and databases do:

    READ = 1 (bit 0)    WRITE = 2 (bit 1)    EXEC = 4 (bit 2)    ADMIN = 8 (bit 3)

Permissions are passed around as letters: "r", "w", "x", "a", e.g. "rw".

    p = Permissions()
    p.grant("ana", "rw")
    p.grant("ben", "r")
    p.has("ana", "rw")       ->  True        has ALL of the given letters
    p.has("ben", "rw")       ->  False
    p.describe("ana")        ->  "rw--"      fixed order r, w, x, a with "-" for missing
    p.revoke("ana", "w")
    p.describe("ana")        ->  "r---"
    p.users_with("r")        ->  ["ana", "ben"]     sorted names that have ALL the letters
    p.mask("ana")            ->  1

Rules:
  - Unknown users have no permissions (mask 0, describe "----").
  - grant/revoke with letters a user already has (or doesn't have) is fine.
  - has(user, "") is True.

Hint:     A dict from letter to bit. grant: mask |= bits, revoke: mask &= ~bits,
          has: mask & bits == bits.
"""

READ, WRITE, EXEC, ADMIN = 1, 2, 4, 8


class Permissions:
    def __init__(self):
        raise NotImplementedError

    def grant(self, user: str, letters: str) -> None:
        raise NotImplementedError

    def revoke(self, user: str, letters: str) -> None:
        raise NotImplementedError

    def has(self, user: str, letters: str) -> bool:
        raise NotImplementedError

    def describe(self, user: str) -> str:
        raise NotImplementedError

    def users_with(self, letters: str) -> list[str]:
        raise NotImplementedError

    def mask(self, user: str) -> int:
        raise NotImplementedError


CLASS = "Permissions"

USES = ["bits.shift_mask"]

TESTS = [
    ([("Permissions",), ("grant", "ana", "rw"), ("grant", "ben", "r"), ("has", "ana", "rw"), ("has", "ben", "rw"),
      ("describe", "ana"), ("revoke", "ana", "w"), ("describe", "ana"), ("users_with", "r"), ("mask", "ana")],
     [None, None, None, True, False, "rw--", None, "r---", ["ana", "ben"], 1]),
    ([("Permissions",), ("describe", "ghost"), ("mask", "ghost"), ("has", "ghost", ""), ("has", "ghost", "r")],
     [None, "----", 0, True, False]),
    ([("Permissions",), ("grant", "root", "rwxa"), ("mask", "root"), ("revoke", "root", "xx"), ("describe", "root"),
      ("grant", "root", "x"), ("describe", "root"), ("users_with", "wa")],
     [None, None, 15, None, "rw-a", None, "rwxa", ["root"]]),
    ([("Permissions",), ("grant", "b", "x"), ("grant", "a", "xr"), ("grant", "c", "w"), ("users_with", "x"),
      ("users_with", ""), ("revoke", "c", "rwxa"), ("mask", "c")],
     [None, None, None, None, ["a", "b"], ["a", "b", "c"], None, 0]),
]
