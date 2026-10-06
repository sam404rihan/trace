def format_table(rows: list[list[str]]) -> list[str]:
    def is_number(cell):
        try:
            float(cell)
            return True
        except ValueError:
            return False

    header, body = rows[0], rows[1:]
    cols = len(header)
    body = [row + [""] * (cols - len(row)) for row in body]          # pad short rows
    widths = [max(len(r[c]) for r in [header] + body) for c in range(cols)]

    lines = [" | ".join(h.ljust(w) for h, w in zip(header, widths)).rstrip(),
             "-+-".join("-" * w for w in widths)]
    for row in body:
        cells = [cell.rjust(w) if is_number(cell) else cell.ljust(w) for cell, w in zip(row, widths)]
        lines.append(" | ".join(cells).rstrip())
    return lines
