from pathlib import Path

import aiofiles
import aiohttp

from reddit.api import Media

BASE_DIR = Path(__file__).resolve().parent.parent


async def download_medias(medias: list[Media]) -> None:
    """Скачивает и сохраняет множество медиафайлов из источников."""
    for media in medias:
        await download(media.media_url,
                       media.filename)
    

async def download(url: str, filename: str) -> None:
    """Скачивает и сохраняет файл из источника."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(
                        f"{BASE_DIR}/media/{filename}",
                        mode="wb")
                await f.write(await resp.read())
                await f.close()

