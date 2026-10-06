def closest_k_values(root: TreeNode, target: float, k: int) -> list[int]:
    window = deque()                # up to k values, in increasing order
    stack, node = [], root
    while stack or node:            # iterative in-order: values come out sorted
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if len(window) < k:
            window.append(node.val)
        elif abs(node.val - target) < abs(window[0] - target):
            window.popleft()        # the new value beats the oldest (furthest left) one
            window.append(node.val)
        else:
            break                   # values only get further from target from here on
        node = node.right
    return list(window)
