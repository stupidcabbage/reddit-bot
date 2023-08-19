import asyncio 

from db import execute, fetch_one, close_db, _async_close_db, fetch_all
from services.subreddits import Subreddit, get_all_subreddits_without_posts as gs
from services.posts import insert_post, post_is_exists, Post, _get_post_base_sql, NoDBPost, _get_post_from_db
from services.flairs import Flair

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

