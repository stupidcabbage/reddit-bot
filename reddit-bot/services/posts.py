from dataclasses import dataclass
from typing import Iterable, LiteralString

from db import execute, fetch_all, fetch_one
from services.flairs import Flair
from services.medias import Media
from services.subreddits import Subreddit


@dataclass
class Post:
    id: int
    title: str
    description: str | None
    flair: Flair | None
    subreddit: Subreddit
    created_at: str
    media: Iterable[Media] | None
    is_published: bool = False


async def insert_post(title: str,
                      description: str,
                      subreddit: Subreddit,
                      flair: Flair) -> Post:
   await execute(
        """
        INSERT OR IGNORE INTO posts (title, description,
                                     subreddit_id, flair_name)
        VALUES (:title, :description, :subreddit_id, :flair_name);""",
        {"title": title,
         "description": description,
         "subreddit_id": subreddit.id,
         "flair_name": flair.name},
    )
   return await get_post_from_db(title, description, subreddit)


async def assign_post_is_published(post: Post) -> None:
    await execute("UPDATE posts SET is_published=true WHERE id=:id",
                  {"id": post.id})


async def is_post_published(post: Post) -> bool:
    result = await fetch_one(
            """
            SELECT count(*)
            FROM posts
            WHERE id=:id AND is_published=true;
            """,
            {"id": post.id})
    return bool(result["count(*)"])


async def get_post_from_db(title: str,
                           description: str,
                           subreddit: Subreddit,
                           media: Iterable[Media] | None = None) -> Post | None:
    r_post = await fetch_all(
        f"""
        {_get_post_base_sql()}
        WHERE p.title=:title and p.subreddit_id=:subreddit_id
        and p.description=:description;""",
        {"title": title,
         "subreddit_id": subreddit.id,
         "description": description},)

    if not r_post:
        return None

    if r_post[0]["filename"]:
        media = [Media(media_url=p["media_url"],
                        filename=p["filename"],
                        file_type=p["file_type"],
                        server_media_id=p["server_media_id"])
                  for p in r_post]

    r_post = r_post[0]
    return Post(
                id=r_post["post_id"],
                title=r_post["title"],
                description=r_post["description"],
                flair=Flair(name=r_post["flair_name"]),
                subreddit=Subreddit(
                   id=r_post["subreddit_id"],
                   name=r_post["subreddit_name"],
                   flairs=None),
                created_at=r_post["created_at"],
                media=media) 


def _get_post_base_sql(
        select_param: LiteralString | None = None) -> LiteralString:
    return f"""
        SELECT
            p.id as post_id,
            s.id as subreddit_id,
            s.name as subreddit_name, 
            {select_param + "," if select_param else ""}
            p.title, p.description,
            p.flair_name, p.created_at,
            m.filename, m.media_url,
            m.file_type, m.server_media_id,
            p.is_published
        FROM posts p
        LEFT JOIN subreddits s ON p.subreddit_id=s.id
        LEFT JOIN medias m ON m.post_id=p.id
    """
