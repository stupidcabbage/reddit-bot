from dataclasses import dataclass


@dataclass
class Media:
    media_url: str
    format_file: str
    filename: str
    file_type: str


@dataclass
class Post:
    title: str
    description: str
    media: list[Media]


