import asyncio
import sys
import time

from loguru import logger
from reddit.api import get_new_posts_from_subreddit as gs
from services.subreddits import get_all_subreddits_without_posts as get_subr
from vk.wall import publish_post
from services.posts import assign_post_is_published, is_post_published
logger.remove()
logger.add(sys.stderr, level="INFO")


async def main():
    while True:
        subreddits = await get_subr()
        for subreddit in subreddits:
            posts = await gs(subreddit, limit=1)
            for post in posts:
                if not await is_post_published(post):
                    await publish_post(post) 
                else:
                    logger.warning(f"Post: {post.title} from {post.subreddit.name} is exists")
            time.sleep(10)

asyncio.get_event_loop().run_until_complete(main())
