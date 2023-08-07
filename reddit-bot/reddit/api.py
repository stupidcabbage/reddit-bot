import praw
from services.translate import translate_text as _
from dotenv import load_dotenv
import os

from typing import List


load_dotenv()

reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET_ID"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
        )


def get_media_from_post(post) -> List[str]:
    """Возвращает все медиа файлы из поста."""
    media_url = []
    if post.secure_media:
        return [post.secure_media['reddit_video']['fallback_url']]
    elif hasattr(post, "preview"):
        for media in post.preview['images']:
            media_url.append(media['source']['url'])
        return media_url
    elif hasattr(post, "media_metadata"):
        for media in post.media_metadata:
            media_url.append(post.media_metadata[media]['s']['u'])
        return media_url
    return []


def get_new_posts_from_subreddit(sreddit: str, limit: int=5):
    """Возвращает список новых постов с сабреддита."""
    posts = reddit.subreddit(sreddit).new(limit=limit)
    posts_stack = []
    for post in posts:
        title = _(post.title)
        description = _(post.selftext)
        media_url = get_media_from_post(post)
        posts_stack.append(
                {"title": title,
                 "description": description,
                 "media": media_url}
                )
    return posts_stack

