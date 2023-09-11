import os

from reddit_bot.config import BASE_DIR


async def delete_file(filename: str, path: str = f"{BASE_DIR}/media/") -> None:
    """Удаляет файл. По умолчанию из директории media/"""
    os.remove(f"{path}{filename}")
