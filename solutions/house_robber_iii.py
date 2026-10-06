def house_robber_iii(root) -> int:
    def best(node):
        """(best if this node is robbed, best if it isn't)"""
        if node is None:
            return 0, 0
        l_rob, l_skip = best(node.left)
        r_rob, r_skip = best(node.right)
        rob = node.val + l_skip + r_skip            # robbing me forces my children to be skipped
        skip = max(l_rob, l_skip) + max(r_rob, r_skip)
        return rob, skip
    return max(best(root))
