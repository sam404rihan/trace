def render_folders(folder: dict) -> list[str]:
    def walk(node):
        """Return (lines for this folder, total size). Children's lines get indented by 2."""
        body, total = [], 0
        for sub in sorted(node["folders"], key=lambda f: f["name"]):
            lines, size = walk(sub)          # trust the recursion for the whole sub-tree
            body += ["  " + line for line in lines]
            total += size
        for name in sorted(node["files"]):
            size = node["files"][name]
            body.append(f"  {name} ({size})")
            total += size
        return [f"{node['name']}/ ({total})"] + body, total

    return walk(folder)[0]
