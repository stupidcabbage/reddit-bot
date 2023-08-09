from reddit.classes import Media, Post
from services.translate import translate_text as _

from . import reddit


def get_media_from_post(post) -> list[Media]:
    """Возвращает все медиа файлы из поста."""
    media_url = []
    if post.secure_media: # Сохранение ссылки видео
        file = post.secure_media[
                "reddit_video"]["scrubber_media_url"].split("/")
        url = post.secure_media["reddit_video"]["fallback_url"]
        return [Media(media_url=url,
                      filename=file[-1],
                      file_type="video")]
    elif hasattr(post, "preview"):
        for media in post.preview['images']:
            url = media["source"]["url"]
            file = url.split("?auto")[0].split("/")
            media_url.append(Media(
                media_url=url,
                filename=file[-1],
                file_type="image"))
        return media_url
    elif hasattr(post, "media_metadata"):
        for media in post.media_metadata:
            url = post.media_metadata[media]['s']['u']
            filename = url.split("?auto")[0].split("/")[3].split("?")[0]
            media_url.append(Media(
                media_url=url,
                filename=filename,
                file_type="image"))
        return media_url
    return []


def get_new_posts_from_subreddit(sreddit: str,
                                 limit: int=5) -> list[Post]:
    """Возвращает список новых постов с сабреддита."""
    reddit_posts = reddit.subreddit(sreddit).new(limit=limit)
    posts = []
    for post in reddit_posts:
        title = _(post.title)
        description = _(post.selftext)
        media = get_media_from_post(post)
        posts.append(Post(title=title, description=description, media=media))
    return posts

