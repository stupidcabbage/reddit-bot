from typing import Iterable

import requests
from reddit_bot.config import BASE_DIR, VK_GROUP_ID
from requests_toolbelt.multipart.encoder import MultipartEncoder
from reddit_bot.services.download_photo import download_medias
from reddit_bot.services.file import delete_file
from reddit_bot.services.medias import Media
from reddit_bot.vk.vk_config import api
import subprocess


async def upload_media_files_to_vk_servers(medias: Iterable[Media]) -> list[int]:
    """
    Функция скачивает медиафайлы с стороннего сервера по ссылке,
    затем заливает данные медиафайлы на сервера ВКонтакте.
    Полученные медиафайлы удаляются. Возвращает MEDIA_ID файлов,
    для дальнейшей работы с ними.
    """
    await download_medias(medias)
    ids = await upload_medias(medias)
    for media in medias:
        await delete_file(f"{media.filename}")
        if media.audio_url:
            await delete_file(f"audio_{media.filename[6:]}")
            await delete_file(f"{media.filename[6:]}")
    return ids


async def upload_medias(medias: Iterable[Media]) -> list[int]:
    """Загружает полученные медиафайлы на сервер
    и возвращает их ID на сервере."""
    ids = []
    if medias[0].file_type == "video":
        cmd = 'ffmpeg -y -i %s -i %s -c:v copy -c:a aac -strict experimental %s' % (f"{BASE_DIR}/media/{medias[0].filename}", f"{BASE_DIR}/media/audio_{medias[0].filename}", f"{BASE_DIR}/media/result{medias[0].filename}")
        subprocess.call(cmd, shell=True)
        medias[0].filename = "result" + medias[0].filename
        upload_url = await api.video.save(is_private=1,
                                          privacy_view=0)
        server_info = upload_photo_to_server(upload_url.upload_url, medias)
        return [server_info.get("video_id")]
    elif medias[0].file_type == "image":
        upload_url = await api.photos.get_wall_upload_server(VK_GROUP_ID)
        server_info = upload_photo_to_server(upload_url.upload_url, medias)
        server_medias_id = await api.photos.save_wall_photo(
                photo=server_info.get("photo"),
                group_id=VK_GROUP_ID,
                server=server_info.get("server"),
                hash=server_info.get("hash"))
        for media_id in server_medias_id:
            ids.append(media_id.id)
        return ids


def upload_photo_to_server(url: str, medias: Iterable[Media]) -> dict:
    """Передает файлы на сервер, используя ссылку,
    полученную в get_wall_upload_server."""
    mp_encoder = encoding_images(medias)
    response = requests.post(
            url=url,
            data=mp_encoder,
            headers={'Content-Type': mp_encoder.content_type}
        )
    return response.json()


def encoding_images(medias: Iterable[Media]) -> MultipartEncoder:
    """Формирует словарь изображений для передачи в запросе."""
    images = {}
    for i, media in enumerate(medias):
        name_image = "file" + str(i)
        path_to_file = f'{BASE_DIR}/media/{media.filename}'
        images[name_image] = (
                path_to_file,
                open(path_to_file, 'rb'),
                f'{media.file_type}/{media.filename.split(".")[-1]}')
    return MultipartEncoder(fields=images)
