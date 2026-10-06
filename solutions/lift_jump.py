def lift_jump(up: list[list[int]], v: int, k: int) -> int:
    for j in range(len(up)):
        if k >> j & 1:
            v = up[j][v]
            if v == -1:
                return -1
    return v if k < (1 << len(up)) else -1
