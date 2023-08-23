from vk.media import upload_media_files_to_vk_servers
from vk.vk_config import api
from config import VK_OWNER_ID, VK_USER_ID, VK_GROUP_ID
from typing import LiteralString, Iterable
from services.posts import Post, assign_post_is_published


async def publish_post(post: Post,
                       attachments: Iterable[str] | None = None ):
    try:
        if post.media:
            ids = await upload_media_files_to_vk_servers(post.media)
            attachments = _make_attachment_string(post, ids)
        await api.wall.post(owner_id=-220785898,
                            message=post.title,
                            attachments=attachments)
    finally:
        await assign_post_is_published(post)


def _make_attachment_string(post: Post, 
                            ids_media: list[int]) -> LiteralString:
    if post.media[0].file_type == "video":
        vk_owner_id = VK_OWNER_ID
        file_type = "video"
    else:
        vk_owner_id = VK_USER_ID
        file_type = "photo"

    attachments = ""
    for id in ids_media:
        attachments += f"{file_type}{vk_owner_id}_{id},"
    return attachments[:-1]
  
 
