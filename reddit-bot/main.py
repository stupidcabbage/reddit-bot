import asyncio
import time

from reddit.api import get_new_posts_from_subreddit as gs
from services.subreddits import get_all_subreddits_without_posts as get_subr
from vk.wall import publish_post


async def main():
    while True:
        subreddits = await get_subr()
        for subreddit in subreddits:
            posts = await gs(subreddit, limit=1)
            for post in posts:
                await publish_post(post)
        time.sleep(10)


asyncio.get_event_loop().run_until_complete(main())
