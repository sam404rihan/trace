def min_add_parens(s: str) -> int:
    # One counter for the unclosed "(": a ")" with nothing open needs an added "(". O(n).
    open_ = added = 0
    for ch in s:
        if ch == "(":
            open_ += 1
        elif open_:
            open_ -= 1
        else:
            added += 1                      # this ")" needs a "(" before it
    return added + open_                    # each "(" still open needs a ")"
