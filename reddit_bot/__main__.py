import asyncio
import time

from reddit_bot.reddit.api import get_new_posts_from_subreddit as gs
from reddit_bot.services.subreddits import get_all_subreddits_without_posts as get_subr
from reddit_bot.vk.wall import publish_post
from reddit_bot.db import close_db

async def main():
    while True:
        subreddits = await get_subr()
        for subreddit in subreddits:
            posts = await gs(subreddit, limit=1)
            for post in posts:
                await publish_post(post)
        time.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    finally:
        close_db()

