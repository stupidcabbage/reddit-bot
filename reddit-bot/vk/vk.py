from vkbottle import API
from dotenv import load_dotenv
import os
import asyncio
import aiohttp


load_dotenv()


api = API(token=os.getenv("VK_ACCESS_TOKEN"))


async def upload_photos_to_server(url: str, *args: str):
    """Передает фотографии на сервер по ссылке,
    полученной методом get_wall_upload_server."""
    async with aiohttp.ClientSession() as session:
        response = await session.post(
                url=url,
                data=mp_encoder,
                headers={"Contnet-Type": mp_encoder.content_type})
        return await response.json()


async def get_server():
    data = await api.photos.get_wall_upload_server(os.getenv("VK_GROUP_ID"))
    print(data.upload_url)



asyncio.run(get_server())

