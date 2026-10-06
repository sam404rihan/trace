from functools import lru_cache


@lru_cache(maxsize=None)    # memo: each (rows, cols) is computed once, so rows * cols calls in total
def count_paths(rows: int, cols: int) -> int:
    if rows == 1 or cols == 1:
        return 1
    # The last move came from above or from the left.
    return count_paths(rows - 1, cols) + count_paths(rows, cols - 1)
