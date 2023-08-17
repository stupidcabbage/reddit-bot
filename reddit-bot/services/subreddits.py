from dataclasses import dataclass
from services.flairs import Flair
from services.posts import Post
from db import fetch_all


@dataclass
class Subreddit:
    id: int
    name: str
    posts: list[Post] | None
    flairs: list[Flair] | None


async def get_all_subreddits_without_posts() -> list[Subreddit] | None:
    sql = """
    SELECT s.*, f.id AS flair_id, f.name AS flair_name
    FROM subreddits s
    LEFT JOIN flairs f ON s.id=f.subreddit_id;"""
    subreddits = await fetch_all(sql)
    if not subreddits:
        return None
 
    return await _build_subreddits(subreddits)


async def _build_subreddits(db_subreddits: list[dict]) -> list[Subreddit]:
    subreddits = []
    for subreddit in db_subreddits:
        subr = _build_subreddit(subreddit)
        if subreddits and subr.name == subreddits[-1].name:
            subreddits[-1].flairs.append(subr.flairs[0])
        else:
            subreddits.append(subr)

    return subreddits


def _build_subreddit(subreddit_db_rows: dict,
                     flair: Flair | None = None)-> Subreddit:
    if subreddit_db_rows.get("flair_name"):
        flair = Flair(id=subreddit_db_rows["flair_id"],
                      name=subreddit_db_rows["flair_name"])
    return Subreddit(
            id=subreddit_db_rows["id"],
            name=subreddit_db_rows["name"],
            posts=None,
            flairs=[flair]
            )
        
