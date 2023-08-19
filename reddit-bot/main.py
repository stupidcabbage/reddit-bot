import asyncio
import sys
import time

from config import VK_OWNER_ID, VK_USER_ID
from loguru import logger
from reddit.api import get_new_posts_from_subreddit as gs
from services.subreddits import get_all_subreddits_without_posts as get_subr
from vk.media import api, upload_media_files_to_vk_servers

logger.remove()
logger.add(sys.stderr, level="INFO")


async def test(post):
    attachments = ''
    if post.media:
        ids = await upload_media_files_to_vk_servers(post.media)
        vk_owner_id = VK_OWNER_ID if post.media[0].file_type == "video" else VK_USER_ID 
        for id in ids:
            attachments += f'{"video" if post.media[0].file_type == "video" else "photo"}{vk_owner_id}_{id},'
        await api.wall.post(owner_id=-220785898, message=post.title,
                            attachments=attachments[:-1])
    else:
        await api.wall.post(owner_id=-220785898,
                            message=post.title)

all_posts = []
async def main():
    while True:
        subreddits = await get_subr()
        for subreddit in subreddits:
            posts = await gs(subreddit, limit=1)
            for post in posts:
                if post not in all_posts:
                    all_posts.append(post)
                    await test(post)
                else:
                    logger.warning("No that try")
            time.sleep(10)
            logger.warning(all_posts)

asyncio.get_event_loop().run_until_complete(main())
