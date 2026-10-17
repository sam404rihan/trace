def min_suffix_flips(target: str) -> int:
    # The first wrong bulb forces a press there. A bulb is on when the presses so far are odd. O(n).
    presses = 0
    for want in target:
        on = presses % 2 == 1
        if on != (want == "1"):
            presses += 1
    return presses
