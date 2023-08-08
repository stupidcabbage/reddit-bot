from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
VK_GROUP_ID = os.getenv("VK_GROUP_ID")
VK_TOKEN = os.getenv("VK_ACCESS_TOKEN")
VK_OWNER_ID = os.getenv("VK_OWNER_ID")
VK_USER_ID = os.getenv("VK_USER_ID")
