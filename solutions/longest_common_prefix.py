def longest_common_prefix(words: list[str]) -> str:
    # Walk the words column by column; stop at the first column that differs.
    prefix = []
    for column in zip(*words):           # zip stops at the shortest word
        if len(set(column)) != 1:
            break
        prefix.append(column[0])
    return "".join(prefix)

    # Standard library: os.path.commonprefix(words) does exactly this.
