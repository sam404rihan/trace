def max_xor_pair(nums: list[int]) -> int:
    best = 0
    for shift in range(30, -1, -1):             # decide the answer's bits from the top down
        candidate = best | (1 << shift)         # can this bit be 1 too?
        prefixes = {x >> shift for x in nums}
        target = candidate >> shift
        # Two prefixes a, b with a ^ b == target exist iff a ^ target is itself a prefix.
        if any(p ^ target in prefixes for p in prefixes):
            best = candidate
    return best
