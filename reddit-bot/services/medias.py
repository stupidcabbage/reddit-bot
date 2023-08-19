from dataclasses import dataclass

from db import execute


@dataclass
class Media:
    media_url: str
    filename: str
    file_type: str
    server_media_id: int | None = None


async def insert_media(post, media: Media):
    await execute(
            """INSERT OR IGNORE INTO medias
            VALUES (:filename, :media_url, :file_type, 
                    :server_media_id, :post_id);""",
            {"filename": media.filename,
             "media_url": media.media_url,

             "file_type": media.file_type,
             "server_media_id": media.server_media_id,
             "post_id": post.id},
            ) 
