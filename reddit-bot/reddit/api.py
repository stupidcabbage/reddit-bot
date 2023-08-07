import praw

import pprint
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET_ID"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
        )


top_posts = reddit.subreddit("FortniteMemes").new(limit=10)
for post in top_posts:
    print(post.selftext_html)
