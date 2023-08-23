from templates import render_template
from services.posts import Post
from services.subreddits import Subreddit
from services.flairs import Flair
import asyncio

post = Post(
        id=1,
        title="ДЛИННЫЙ ТАЙТЛ С СУПЕР КРУТЫМИ ДИАЛОГАМИ",
        description="КРУТОЙ ДЕКСКРИПШИН",
        flair=Flair(name="test"),
        subreddit=Subreddit(id=0, name="TEST SUBREDDIT", flairs=[Flair(name="test")]),
        created_at="123123",
        media=None,
        is_published=False)

async def test():
    result = await render_template("test.j2", data={"post": post})
    return result

print(asyncio.run(test()))
