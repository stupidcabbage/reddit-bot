from typing import Dict

import aiohttp
import aiofiles
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def download_media(urls: Dict[str, str]):
    pass


async def download(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"{BASE_DIR}/media/file.jpg", mode="wb")
                await f.write(await resp.read())
                await f.close()

url = "https://preview.redd.it/sdl5cwurfrgb1.jpg?auto=webp&s=e01eb600c5db913a6ecc86329107039e0c1953d0"

asyncio.run(download(url))
