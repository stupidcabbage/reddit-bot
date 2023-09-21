from typing import Iterable
from reddit_bot.services.flairs import Flair
from reddit_bot.services.logging import debug_logger, info_logging
from reddit_bot.services.medias import Media, insert_media
from reddit_bot.services.posts import Post, insert_post
from reddit_bot.services.subreddits import Subreddit
from reddit_bot.services.translate import translate_text as _

from reddit_bot.reddit import reddit

import loguru

@info_logging
async def get_new_posts_from_subreddit(subreddit: Subreddit,
                                       limit: int = 5) -> Iterable[Post]:
    """Возвращает список новых постов с сабреддита."""
    reddit_posts = await reddit.subreddit(subreddit.name)
    posts = []
    async for post in reddit_posts.new(limit=limit):
        db_post = await insert_post(
                await _(post.title),
                await _(post.selftext),
                subreddit,
                Flair(post.link_flair_text))

        media = await _get_media_from_post(post, db_post)
        db_post.media = media
        if _is_post_flair_exists(subreddit, db_post):
            posts.append(db_post)
    return posts


@debug_logger
async def _get_media_from_post(post, db_post) -> Iterable[Media] | None:
    """Возвращает все медиа файлы из поста."""
    media_url = []
    if post.is_video:
        url = post.media["reddit_video"]["fallback_url"]
        audio_url = url[:url.rfind('/')] + '/DASH_AUDIO_128.mp4'
        filename = post.media["reddit_video"]["scrubber_media_url"].split(
                "/")[-1]
        media_url.append(Media(
            media_url=url,
            audio_url=audio_url,
            filename=filename,
            file_type="video"))
    elif hasattr(post, "is_gallery") and post.is_gallery:
        for x in post.gallery_data["items"]:
            media_id = x["media_id"]
            extension = post.media_metadata[media_id]["m"].split("/")[-1]
            media_url.append(Media(
                media_url=f"https://i.redd.it/{media_id}.{extension}",
                filename=f"{media_id}.{extension}",
                file_type="image"
                ))
    elif hasattr(post, "post_hint") and post.post_hint == "image":
        media_url.append(Media(
            media_url=post.url,
            filename=post.url.split("/")[-1],
            file_type=post.post_hint
            ))
    for media in media_url:
        await insert_media(db_post, media)
    return media_url


def _is_post_flair_exists(subreddit: Subreddit,
                          post: Post) -> bool:
    loguru.logger.warning(post.flair)
    loguru.logger.warning(subreddit.flairs)
    loguru.logger.warning(Flair("all") in subreddit.flairs)
    return (subreddit.flairs and post.flair in subreddit.flairs
            or Flair("all") in subreddit.flairs)

