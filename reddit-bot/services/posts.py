from dataclasses import dataclass
from services.flairs import Flair
from reddit.classes import Media


@dataclass
class Post:
    id: int
    title: str
    description: str
    media: list[Media]
    flairs: list[Flair]
    created_at: str
