def chinese_remainder(rems: list[int], mods: list[int]) -> int:
    r, m = 0, 1                         # so far: x ≡ r (mod m)
    for r2, m2 in zip(rems, mods):
        g = gcd(m, m2)
        diff = r2 - r
        if diff % g:
            return -1                   # the two conditions contradict each other
        step = m2 // g
        # x = r + m * t with m * t ≡ diff (mod m2)  <=>  (m/g) * t ≡ diff/g (mod m2/g)
        t = (diff // g) * pow(m // g, -1, step) % step if step > 1 else 0
        r += m * t
        m = m // g * m2                 # lcm(m, m2)
        r %= m
    return r
