import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


VK_GROUP_ID: int = os.getenv("VK_GROUP_ID", 0)
VK_TOKEN: str = os.getenv("VK_ACCESS_TOKEN", "")
VK_OWNER_ID: int = os.getenv("VK_OWNER_ID", 0)
VK_USER_ID: int = os.getenv("VK_USER_ID", 0)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET_ID = os.getenv("REDDIT_SECRET_ID")
REDDIT_REDIRECT_URI = os.getenv("REDDIT_REDIRECT_URI")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"
