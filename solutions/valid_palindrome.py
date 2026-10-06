def valid_palindrome(s: str) -> bool:
    # Two pointers moving inwards, skipping non-alphanumerics. O(n) time, O(1) space.
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True

    # Simpler but O(n) space:
    #   cleaned = [c.lower() for c in s if c.isalnum()]
    #   return cleaned == cleaned[::-1]
