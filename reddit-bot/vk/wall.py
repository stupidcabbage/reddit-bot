from typing import Iterable, LiteralString

from config import VK_GROUP_ID, VK_OWNER_ID, VK_USER_ID, TEMPLATES_DIR
from services.posts import Post, assign_post_is_published, is_post_published
from vk.media import upload_media_files_to_vk_servers
from vk.vk_config import api
from templates import render_template
from os import path
from services.logging import info_logging


class PostExists(Exception):
    def __str__(self):
        return "Post is already exists."


@info_logging
async def publish_post(post: Post):
    if not await is_post_published(post):
        await _publish_post(post)
    else:
        raise PostExists


async def _publish_post(post: Post,
                       attachments: Iterable[str] | None = None):
    try:
        if post.media:
            ids = await upload_media_files_to_vk_servers(post.media)
            attachments = _make_attachment_string(post, ids)
        message = await _render_message(post)
        await api.wall.post(owner_id=-220785898,
                            message=message,
                            attachments=attachments)
    finally:
        await assign_post_is_published(post)


async def _render_message(post: Post) -> str:
    if post.flair.name:
        template_name = f"{post.flair.name.lower().replace(' ', '')}{post.subreddit.name.lower().replace(' ', '')}.j2"
        if path.exists(TEMPLATES_DIR / template_name):
            return await render_template(template_name, {"post": post})
    return await render_template("content.j2", {"post": post})


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
  
 
