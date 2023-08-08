import praw
from services.translate import translate_text as _
from dotenv import load_dotenv
import os
from dataclasses import dataclass

from typing import List, Dict


load_dotenv()

reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET_ID"),
        redirect_uri=os.getenv("REDDIT_REDIRECT_URI"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
        )

@dataclass
class Media:
    media_url: str
    format_file: str


@dataclass
class Post:
    title: str
    description: str
    media: list[Media]


def get_media_from_post(post) -> list[Media]:
    """Возвращает все медиа файлы из поста."""
    media_url = []
    if post.secure_media:
        format_file = post.secure_media[
                "reddit_video"]["scrubber_media_url"].split(".")[-1]
        url = post.secure_media["reddit_video"]["fallback_url"]
        return [Media(media_url=url, format_file=format_file)]
    elif hasattr(post, "preview"):
        for media in post.preview['images']:
            url = media["source"]["url"]
            format_file = url.split("?auto")[0].split(".")[-1]
            media_url.append(Media(media_url=url, format_file=format_file))
        return media_url
    elif hasattr(post, "media_metadata"):
        for media in post.media_metadata:
            url = post.media_metadata[media]['s']['u']
            format_file = post.media_metadata[media]["m"].split("/")[-1]
            media_url.append(Media(media_url=url, format_file=format_file))
        return media_url
    return []


def get_new_posts_from_subreddit(sreddit: str,
                                 limit: int=5) -> List[Dict[str, str]]:
    """Возвращает список новых постов с сабреддита."""
    reddit_posts = reddit.subreddit(sreddit).new(limit=limit)
    posts = []
    for post in reddit_posts:
        title = _(post.title)
        description = _(post.selftext)
        media = get_media_from_post(post)
        posts.append(Post(title=title, description=description, media=media))
    return posts

