def multiply_strings(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"
    res = [0] * (len(a) + len(b))
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            res[i + j + 1] += int(a[i]) * int(b[j])   # long multiplication, no carry yet
    for k in range(len(res) - 1, 0, -1):              # one sweep of carries, right to left
        res[k - 1] += res[k] // 10
        res[k] %= 10
    return "".join(map(str, res)).lstrip("0")
