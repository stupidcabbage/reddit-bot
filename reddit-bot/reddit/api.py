import praw
from dotenv import load_dotenv
import os

load_dotenv()

SUBREDDITS = ["FortniteLeaks"]

reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET_ID"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
        )

for sreddit in SUBREDDITS:
    posts = reddit.subreddit(sreddit).new(limit=10)
    for post in posts:
        print("TITLE: ", post.title)
        print("DESCRIPTION: ", post.selftext)
        try: media_data = post.media_metadata
        except AttributeError: media_data = None
        if media_data:
            for media in media_data:
                print("MEDIA: ", media_data[media]['s']['u'])
