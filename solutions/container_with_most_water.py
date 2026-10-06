def container_with_most_water(height: list[int]) -> int:
    # Start widest; always move the shorter line inwards. O(n).
    # Why: the area is capped by the shorter line. Moving the taller one
    # only shrinks the width without raising that cap, so it can't help.
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
