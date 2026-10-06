def digit_choices(digits: list[int], i: int, tight: bool) -> list[tuple[int, bool]]:
    top = digits[i] if tight else 9
    return [(d, tight and d == top) for d in range(top + 1)]
