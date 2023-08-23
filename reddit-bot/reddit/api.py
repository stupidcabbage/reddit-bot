from typing import Iterable

from services.flairs import Flair
from services.medias import Media, insert_media
from services.posts import Post, insert_post
from services.subreddits import Subreddit
from services.translate import translate_text as _

from . import reddit


async def get_new_posts_from_subreddit(subreddit: Subreddit,
                                       limit: int=5) -> Iterable[Post]:
    """Возвращает список новых постов с сабреддита."""
    reddit_posts = await reddit.subreddit(subreddit.name)
    posts = []
    async for post in reddit_posts.new(limit=limit):
        title = _(post.title)
        description = _(post.selftext)
        flair = Flair(post.link_flair_text)

        db_post = await insert_post(title, description, subreddit, flair)
        media = await _get_media_from_post(post, db_post)
        db_post.media = media
        posts.append(db_post)
    return posts


async def _get_media_from_post(post, db_post) -> Iterable[Media] | None:
    """Возвращает все медиа файлы из поста."""
    media_url = []
    if hasattr(post.secure_media, "reddit_video"):  # Сохранение ссылки видео
        file = post.secure_media[
                "reddit_video"]["scrubber_media_url"].split("/")
        url = post.secure_media["reddit_video"]["fallback_url"]
        media_url.append(Media(
            media_url=url,
            filename=file[-1],
            file_type="video"))
    elif hasattr(post, "preview"):
        for media in post.preview['images']:
            url = media["source"]["url"]
            file = url.split("?auto")[0].split("/")
            media_url.append(Media(
                media_url=url,
                filename=file[-1],
                file_type="image"))
    elif hasattr(post, "media_metadata"):
        for media in post.media_metadata:
            url = post.media_metadata[media]['s']['u']
            filename = url.split("?auto")[0].split("/")[3].split("?")[0]
            media_url.append(Media(
                media_url=url,
                filename=filename,
                file_type="image"))
    for media in media_url:
        await insert_media(db_post, media)
    return media_url
