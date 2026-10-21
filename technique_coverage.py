"""Technique coverage: every technique a problem uses is taught by exactly one basic problem,
earlier in the course. Pure functions: server.py and the tests feed it the parsed course."""

BASIC_KINDS = {"snippet", "guided", "parsons"}


def is_basic(p):
    return p["kind"] in BASIC_KINDS or p.get("difficulty") == "easy"


def check_coverage(topics, problems, techniques):
    """topics: course order, each {"id", "items"} with items in ladder order. problems: name ->
    {"kind", "difficulty", "uses", "teaches", "audited", "topic_id"}. techniques: id -> {...}.
    Returns (errors, warnings) as plain-English lines. Since Part 2 finished, an unaudited problem is
    an error, so warnings is always empty; it stays in the return value for the callers."""
    errors, warnings = [], []
    order = {name: i for i, name in enumerate(n for t in topics for n in t["items"])}
    tags, teachers = {"uses": {}, "teaches": {}}, {}
    for name in order:
        p = problems[name]
        if not p["audited"]:
            errors.append(f"{name} ({p['topic_id']}): not audited: give it a USES list")
        for field in ("uses", "teaches"):
            ids = p[field]
            if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
                errors.append(f"{name}: {field.upper()} must be a list of technique ids")
                ids = []
            tags[field][name] = ids
            for t in ids:
                if t not in techniques:
                    errors.append(f"{name}: {field.upper()} names {t}, which isn't in course/techniques.py")
        for t in sorted(set(tags["uses"][name]) & set(tags["teaches"][name])):
            errors.append(f"{name}: {t} is in both TEACHES and USES")
        for t in tags["teaches"][name]:
            teachers.setdefault(t, []).append(name)
            if not is_basic(p):
                errors.append(f"{name}: teaches {t}, but a teacher must be a snippet, guided or easy problem "
                              f"(it's {p.get('difficulty') or p['kind']})")
    for t in techniques:
        who = teachers.get(t, [])
        if not who:
            errors.append(f"{t}: no problem teaches it (add it to one basic problem's TEACHES)")
        elif len(who) > 1:
            errors.append(f"{t}: taught by {', '.join(who)}; exactly one problem should teach it")
    for name in order:
        for t in tags["uses"][name]:
            who = teachers.get(t)
            if who and who[0] != name and order[who[0]] > order[name]:
                where = ("later in the same topic" if problems[who[0]]["topic_id"] == problems[name]["topic_id"]
                         else "in a later topic")
                errors.append(f"{name} uses {t}, but its teacher {who[0]} comes {where}")
    return errors, warnings
