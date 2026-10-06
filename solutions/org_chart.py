def org_chart(pairs: list[tuple[str, str]]) -> list[str]:
    reports, employees = {}, set()
    for manager, employee in pairs:
        reports.setdefault(manager, []).append(employee)
        employees.add(employee)
    ceo = next(m for m in reports if m not in employees)

    def walk(person, depth):
        """Return (lines for this person's whole subtree, number of people under them)."""
        lines, under = [], 0
        for r in sorted(reports.get(person, [])):
            sub_lines, sub_under = walk(r, depth + 1)
            lines += sub_lines
            under += 1 + sub_under
        label = f"{person} ({under})" if under else person
        return ["  " * depth + label] + lines, under

    return walk(ceo, 0)[0]
