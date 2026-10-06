def flatten_list(nested: list) -> list[int]:
    # Recursion mirrors the shape of the data: a list may contain lists.
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat


def flatten_generator(nested):
    # Generator version: `yield from` hands back everything the inner call yields.
    for item in nested:
        if isinstance(item, list):
            yield from flatten_generator(item)
        else:
            yield item
