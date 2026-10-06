def text_justify(words: list[str], width: int) -> list[str]:
    lines, cur, letters = [], [], 0
    for w in words:
        if cur and letters + len(cur) + len(w) > width:     # len(cur) = the single spaces needed so far
            lines.append((cur, letters))
            cur, letters = [], 0
        cur.append(w)
        letters += len(w)
    out = []
    for line, letters in lines:
        if len(line) == 1:
            out.append(line[0].ljust(width))
            continue
        base, extra = divmod(width - letters, len(line) - 1)
        text = ""
        for i, w in enumerate(line[:-1]):
            text += w + " " * (base + (i < extra))          # the left gaps take the leftover spaces
        out.append(text + line[-1])
    out.append(" ".join(cur).ljust(width))                  # the last line is left-aligned
    return out
