import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


async def delete_file(filename: str, path: str = f"{BASE_DIR}/media/") -> None:
    """Удаляет файл. По умолчанию из директории media/"""
    os.remove(f"{path}{filename}")

