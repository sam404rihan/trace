def cheapest_flights(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    price = [float("inf")] * n
    price[src] = 0
    for _ in range(k + 1):                      # each round allows one more flight
        nxt = price[:]                          # read last round, write this round
        for a, b, p in flights:
            if price[a] + p < nxt[b]:
                nxt[b] = price[a] + p
        price = nxt
    return price[dst] if price[dst] != float("inf") else -1
