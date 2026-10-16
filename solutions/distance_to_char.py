def distance_to_char(s: str, c: str) -> list[int]:
    # Left pass: distance to the last c on the left. Right pass: keep the smaller of that and
    # the distance to the next c on the right. O(n).
    n = len(s)
    answer = [n] * n
    last = None
    for i in range(n):
        if s[i] == c:
            last = i
        if last is not None:
            answer[i] = i - last
    last = None
    for i in range(n - 1, -1, -1):
        if s[i] == c:
            last = i
        if last is not None:
            answer[i] = min(answer[i], last - i)
    return answer
