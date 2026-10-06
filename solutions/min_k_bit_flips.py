def min_k_bit_flips(bits: list[int], k: int) -> int:
    n = len(bits)
    ends_here = [0] * (n + 1)       # how many flips stop covering bits at this index
    active = moves = 0              # flips currently covering index i
    for i, b in enumerate(bits):
        active -= ends_here[i]
        if b ^ (active & 1) == 0:   # still a 0 after the active flips: a flip must start here
            if i + k > n:
                return -1
            active += 1
            ends_here[i + k] += 1
            moves += 1
    return moves
