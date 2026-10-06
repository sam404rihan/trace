def common_elements(a: list[int], b: list[int]) -> list[int]:
    # Set intersection is O(n + m); sorting the answer adds O(k log k).
    return sorted(set(a) & set(b))

    # The slow version, [x for x in set(a) if x in b], is O(n · m)
    # because `in b` scans the list every time.
