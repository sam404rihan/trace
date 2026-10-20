"""
Design Twitter                                                                [medium]

Build a tiny Twitter:

    post_tweet(user, tweet_id)    the user posts a tweet (ids are unique)
    get_news_feed(user)           the 10 most recent tweet ids posted by the user or by anyone
                                  they follow, newest first
    follow(follower, followee)    start following (following yourself changes nothing)
    unfollow(follower, followee)  stop following (does nothing if they weren't following)

Example:
    t = Twitter()
    t.post_tweet(1, 5)
    t.get_news_feed(1)    ->  [5]
    t.follow(1, 2); t.post_tweet(2, 6)
    t.get_news_feed(1)    ->  [6, 5]
    t.unfollow(1, 2)
    t.get_news_feed(1)    ->  [5]

Aim for:  get_news_feed merging only the newest tweets of each followed user (a heap),
          not sorting every tweet ever posted.
Hint:     Store each user's tweets as a list of (time, id). For the feed, push each relevant user's
          latest tweet into a max-heap (negate the time), pop 10 times, and each pop pushes that
          user's next older tweet.
"""


class Twitter:
    def __init__(self):
        raise NotImplementedError

    def post_tweet(self, user: int, tweet_id: int) -> None:
        raise NotImplementedError

    def get_news_feed(self, user: int) -> list[int]:
        raise NotImplementedError

    def follow(self, follower: int, followee: int) -> None:
        raise NotImplementedError

    def unfollow(self, follower: int, followee: int) -> None:
        raise NotImplementedError


CLASS = "Twitter"


def _sim(ops):
    posts, follows, res = [], {}, [None]
    for op in ops[1:]:
        name, *args = op
        if name == "post_tweet":
            posts.append(tuple(args)); res.append(None)
        elif name == "follow":
            if args[0] != args[1]:
                follows.setdefault(args[0], set()).add(args[1])
            res.append(None)
        elif name == "unfollow":
            follows.get(args[0], set()).discard(args[1]); res.append(None)
        else:
            who = {args[0]} | follows.get(args[0], set())
            res.append([tid for u, tid in reversed(posts) if u in who][:10])
    return res


def _cases():
    import random
    rng = random.Random(73)
    out = []
    for size in (80, 3000):
        ops, tid = [("Twitter",)], 0
        for _ in range(size):
            r = rng.random()
            a, b = rng.randint(1, 6), rng.randint(1, 6)
            if r < 0.45:
                tid += 1
                ops.append(("post_tweet", a, tid))
            elif r < 0.65:
                ops.append(("follow", a, b))
            elif r < 0.75:
                ops.append(("unfollow", a, b))
            else:
                ops.append(("get_news_feed", a))
        out.append((ops, _sim(ops)))
    return out


USES = ["heap.max_negate", "heap.k_way_merge"]

TESTS = [([("Twitter",), ("post_tweet", 1, 5), ("get_news_feed", 1), ("follow", 1, 2), ("post_tweet", 2, 6),
           ("get_news_feed", 1), ("unfollow", 1, 2), ("get_news_feed", 1)],
          [None, None, [5], None, None, [6, 5], None, [5]]),
         ([("Twitter",), ("follow", 1, 1), ("get_news_feed", 1), ("unfollow", 3, 4), ("get_news_feed", 9)],
          [None, None, [], None, []])] + _cases()
