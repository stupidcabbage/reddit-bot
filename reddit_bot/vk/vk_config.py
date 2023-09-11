import sys

from reddit_bot.config import VK_TOKEN
from loguru import logger
from vkbottle import API

logger.remove()
logger.add(sys.stderr, level="INFO")


api = API(token=VK_TOKEN)
