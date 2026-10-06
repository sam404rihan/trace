def valid_paren_string(s: str) -> bool:
    low = high = 0                      # range of possible unmatched "(" counts
    for ch in s:
        if ch == "(":
            low, high = low + 1, high + 1
        elif ch == ")":
            low, high = low - 1, high - 1
        else:
            low, high = low - 1, high + 1
        if high < 0:
            return False                # too many ")" whatever the stars do
        low = max(low, 0)
    return low == 0
