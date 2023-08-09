import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from vkbottle import API

from reddit.classes import Media, Post
from services.download_photo import download_medias
from services.file import delete_file


from . import BASE_DIR, VK_GROUP_ID, VK_TOKEN

api = API(token=VK_TOKEN)


async def upload_media_files_to_vk_servers(medias: list[Media]) -> list[int]:
    """Функция скачивает медиафайлы с стороннего сервера по ссылке,
    затем заливает данные медиафайлы на сервера ВКонтакте.
    Полученные медиафайлы удаляются. Возвращает MEDIA_ID файлов,
    для дальнейшей работы с ними.""" 
    await download_medias(medias)
    ids = await upload_medias(medias)
    for media in medias:
        await delete_file(f"{media.filename}")
    return ids


async def upload_medias(medias: list[Media]) -> list[int]:
    """Загружает полученные медиафайлы на сервер
    и возвращает их ID на сервере."""
    ids = []
    if medias[0].file_type == "video":
        upload_url = await api.video.save(
                group_id=VK_GROUP_ID)
        server_info = upload_photo_to_server(upload_url.upload_url, medias)
        return [server_info.get("video_id")]
    elif medias[0].file_type == "image":
        upload_url = await api.photos.get_wall_upload_server(
                VK_GROUP_ID)
        server_info = upload_photo_to_server(upload_url.upload_url, medias)
        server_medias_id = await api.photos.save_wall_photo(
                photo=server_info.get("photo"),
                group_id=VK_GROUP_ID,
                server=server_info.get("server"),
                hash=server_info.get("hash"))
        for media_id in server_medias_id:
            ids.append(media_id.id)
        return ids

def upload_photo_to_server(url: str, medias: list[Media]) -> dict:
    """Передает файлы на сервер, используя ссылку,
    полученную в get_wall_upload_server."""
    mp_encoder = encoding_images(medias)
    response = requests.post(
            url=url,
            data=mp_encoder,
            headers={'Content-Type': mp_encoder.content_type}
        )
    return response.json()

def encoding_images(medias: list[Media]) -> MultipartEncoder:
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
