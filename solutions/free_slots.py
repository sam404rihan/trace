def free_slots(busy: list[list[list[int]]], day_start: int, day_end: int, min_len: int) -> list[list[int]]:
    # Everyone's busy time, merged into non-overlapping blocks.
    blocks = sorted(iv for person in busy for iv in person)
    merged = []
    for s, e in blocks:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])

    # Walk the day: every gap before a busy block is a free slot.
    slots, cursor = [], day_start
    for s, e in merged:
        if s > cursor:
            slots.append([cursor, min(s, day_end)])
        cursor = max(cursor, e)
        if cursor >= day_end:
            break
    if cursor < day_end:
        slots.append([cursor, day_end])
    return [[s, e] for s, e in slots if e - s >= min_len]
