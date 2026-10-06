class Twitter:
    def __init__(self):
        self.clock = 0
        self.tweets = {}                    # user -> [(time, tweet_id)], oldest first
        self.following = {}                 # user -> set of followees

    def post_tweet(self, user: int, tweet_id: int) -> None:
        self.clock += 1
        self.tweets.setdefault(user, []).append((self.clock, tweet_id))

    def get_news_feed(self, user: int) -> list[int]:
        heap = []
        for u in self.following.get(user, set()) | {user}:
            posts = self.tweets.get(u)
            if posts:
                i = len(posts) - 1          # start from each user's newest tweet
                heappush(heap, (-posts[i][0], posts[i][1], u, i))
        feed = []
        while heap and len(feed) < 10:      # k-way merge, newest first
            _, tid, u, i = heappop(heap)
            feed.append(tid)
            if i > 0:
                t, nxt = self.tweets[u][i - 1]
                heappush(heap, (-t, nxt, u, i - 1))
        return feed

    def follow(self, follower: int, followee: int) -> None:
        if follower != followee:
            self.following.setdefault(follower, set()).add(followee)

    def unfollow(self, follower: int, followee: int) -> None:
        self.following.get(follower, set()).discard(followee)
