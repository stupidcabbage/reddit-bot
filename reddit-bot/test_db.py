import asyncio

from db import _async_close_db, close_db, execute, fetch_all, fetch_one
from services.flairs import Flair
from services.posts import (NoDBPost, Post, _get_post_base_sql,
                            _get_post_from_db, insert_post, post_is_exists)
from services.subreddits import Subreddit
from services.subreddits import get_all_subreddits_without_posts as gs


async def test_function_with_db(sql):
    try:
        result = await fetch_all(sql)
        print(result)
    finally:
        await _async_close_db()

async def test_execute(sql):
    try: 
        post = NoDBPost(title="super_test", description="test_supper",
                        flair=Flair(name="test"), subreddit=Subreddit(id=1, name="FortniteLeaks",
                                                                      flairs=[Flair(name="test")]))
        r_post = await _get_post_from_db(post)
        print(r_post)
    finally:
        await _async_close_db()

asyncio.run(test_execute("INSERT INTO flairs VALUES(3, 'hello world');"))

