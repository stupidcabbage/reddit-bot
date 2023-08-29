from dataclasses import dataclass
from typing import Iterable

from db import fetch_all
from services.flairs import Flair
from services.logging import info_logging

@dataclass
class Subreddit:
    id: int
    name: str
    flairs: Iterable[Flair] | None


@info_logging
async def get_all_subreddits_without_posts() -> Iterable[Subreddit] | None:
    """Возвращает все сабреддиты без постов."""
    sql = """
    SELECT s.*, f.name AS flair_name
    FROM subreddits s
    LEFT JOIN flairs f ON s.id=f.subreddit_id;
    """
    subreddits = await fetch_all(sql)
    if not subreddits:
        return None
 
    return await _build_subreddits(subreddits)


async def _build_subreddits(db_subreddits: list[dict]) -> Iterable[Subreddit]:
    subreddits = []
    for subreddit in db_subreddits:
        subr = _build_subreddit(subreddit)
        if subreddits and subr.name == subreddits[-1].name:
            subreddits[-1].flairs.append(subr.flairs[0])
        else:
            subreddits.append(subr)

    return subreddits


def _build_subreddit(subreddit_db_rows: dict,
                     flair: Flair | None = None) -> Subreddit:
    if subreddit_db_rows.get("flair_name"):
        flair = Flair(name=subreddit_db_rows["flair_name"])
    return Subreddit(
            id=subreddit_db_rows["id"],
            name=subreddit_db_rows["name"],
            flairs=[flair]
            )
        
