from os import path
from typing import Iterable, LiteralString

from config import TEMPLATES_DIR, VK_GROUP_ID, VK_OWNER_ID, VK_USER_ID
from services.exceptions import PostExists
from services.logging import debug_logger, info_logging
from services.posts import Post, assign_post_is_published, is_post_published
from templates import render_template
from vk.media import upload_media_files_to_vk_servers
from vk.vk_config import api


@debug_logger
async def publish_post(post: Post):
    if not await is_post_published(post):
        await _publish_post(post)
    else:
        raise PostExists


@info_logging
async def _publish_post(post: Post,
                       attachments: Iterable[str] | None = None):
    try:
        if post.media:
            ids = await upload_media_files_to_vk_servers(post.media)
            attachments = _make_attachment_string(post, ids)
        message = await _render_message(post)
        await api.wall.post(owner_id=-187577519,
                            message=message,
                            attachments=attachments)
    finally:
        await assign_post_is_published(post)


@debug_logger
async def _render_message(post: Post) -> str:
    if post.flair.name:
        template_name = f"{post.flair.name.lower().replace(' ', '')}{post.subreddit.name.lower().replace(' ', '')}.j2"
        if path.exists(TEMPLATES_DIR / template_name):
            return await render_template(template_name, {"post": post})
    return await render_template("content.j2", {"post": post})


def _make_attachment_string(post: Post, 
                            ids_media: list[int]) -> LiteralString:
    if post.media[0].file_type == "video":
        vk_owner_id = VK_USER_ID
        file_type = "video"
    else:
        vk_owner_id = VK_USER_ID
        file_type = "photo"

    attachments = ""
    for id in ids_media:
        attachments += f"{file_type}{vk_owner_id}_{id},"
    return attachments[:-1]
  
 
