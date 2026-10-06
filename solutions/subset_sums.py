def subset_sums(nums: list[int]) -> list[int]:
    out = [0] * (1 << len(nums))
    for mask in range(1, len(out)):
        low = mask & -mask                                          # the lowest chosen item
        out[mask] = out[mask ^ low] + nums[low.bit_length() - 1]    # reuse the smaller subset
    return out
