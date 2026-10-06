NEEDS, CAMERA, COVERED = 0, 1, 2


def min_cameras(root: TreeNode) -> int:
    cameras = 0

    def state(node):
        """Post-order: what this node tells its parent."""
        nonlocal cameras
        if node is None:
            return COVERED                  # nothing to watch
        left, right = state(node.left), state(node.right)
        if NEEDS in (left, right):
            cameras += 1                    # a child can only be saved from here
            return CAMERA
        if CAMERA in (left, right):
            return COVERED
        return NEEDS                        # leave it to the parent: a camera there covers more

    if state(root) == NEEDS:
        cameras += 1
    return cameras
