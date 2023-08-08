import aiohttp
import aiofiles
from pathlib import Path

from reddit.api import Media


BASE_DIR = Path(__file__).resolve().parent.parent


async def download_medias(medias: list[Media]) -> None:
    """Скачивает медиафайлы и сохраняет их."""
    for media in medias:
        await download(media.media_url,
                       media.filename,
                       media.format_file)
    

async def download(url: str, filename: str, format_file: str) -> None:
    """Скачивает и сохраняет файл из источника."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(
                        f"{BASE_DIR}/media/{filename}.{format_file}",
                        mode="wb")
                await f.write(await resp.read())
                await f.close()

