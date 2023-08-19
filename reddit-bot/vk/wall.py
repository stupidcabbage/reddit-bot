from vk.media import upload_media_files_to_vk_servers
from vk.vk_config import api


async def publish_post(post: Post):
    if post.media:
        ids_media = await upload_media_files_to_vk_servers(post.media)


def _make_attachment_string(ids_media: list[int]):
    
