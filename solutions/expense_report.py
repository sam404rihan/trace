def expense_report(lines: list[str]) -> dict:
    by_cat, by_day = {}, {}
    total, skipped = 0.0, 0
    for line in lines:
        if not line.strip() or line.strip().lower() == "date,category,amount":
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            skipped += 1
            continue
        date, cat, amount = parts
        try:
            value = float(amount)
        except ValueError:
            skipped += 1
            continue
        cat = cat.lower()
        total += value
        by_cat[cat] = by_cat.get(cat, 0) + value
        by_day[date] = by_day.get(date, 0) + value
    # Round at the end, so tiny float errors don't decide the ordering.
    cats = sorted(((c, round(v, 2)) for c, v in by_cat.items()), key=lambda kv: (-kv[1], kv[0]))
    busiest = min(by_day, key=lambda d: (-round(by_day[d], 2), d)) if by_day else None
    return {"total": round(total, 2), "by_category": cats, "busiest_day": busiest, "skipped": skipped}
