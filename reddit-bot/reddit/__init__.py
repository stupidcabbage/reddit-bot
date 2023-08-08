import praw

from dotenv import load_dotenv
import os


load_dotenv()

reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET_ID"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
        )
