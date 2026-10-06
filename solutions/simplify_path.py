def simplify_path(path: str) -> str:
    stack = []
    for part in path.split("/"):
        if part in ("", "."):
            continue                    # "//", trailing "/", and "." change nothing
        if part == "..":
            if stack:
                stack.pop()             # up one folder (but never above the root)
        else:
            stack.append(part)
    return "/" + "/".join(stack)
