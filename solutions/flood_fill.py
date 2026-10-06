def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    # DFS with an explicit stack over cells of the original colour. O(rows · cols).
    original = image[sr][sc]
    if original == color:
        return image                     # nothing to do, and it avoids an endless loop
    rows, cols = len(image), len(image[0])
    stack = [(sr, sc)]
    image[sr][sc] = color
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original:
                image[nr][nc] = color    # recolouring doubles as "visited"
                stack.append((nr, nc))
    return image
