import asyncpraw
from config import (REDDIT_CLIENT_ID, REDDIT_REDIRECT_URI, REDDIT_SECRET_ID,
                    REDDIT_USER_AGENT)
from dotenv import load_dotenv

load_dotenv()

reddit = asyncpraw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET_ID,
        redirect_uri=REDDIT_REDIRECT_URI,
        user_agent=REDDIT_USER_AGENT
        )
