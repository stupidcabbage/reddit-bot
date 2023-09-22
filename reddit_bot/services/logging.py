import sys
from typing import Callable

import decorator
from loguru import logger
from reddit_bot.services.exceptions import PostExists
from reddit_bot.vk.vk_config import api

logger.remove()
logger.add(sys.stderr, level="ERROR")


@decorator.decorator
async def info_logging(fn, *args, **kwargs):
    try:
        logger.info(f"{fn.__name__} has started.")
        return await fn(*args, **kwargs)
    except PostExists:
        logger.info(f"{fn.__name__} post already exists")
    except Exception as e:
        await log_error_message(fn, e)
    finally:
        logger.info(f"{fn.__name__} completed the execution.")


@decorator.decorator
async def debug_logger(fn, *args, **kwargs):
    try:
        logger.debug(f"{fn.__name__} has started.")
        return await fn(*args, **kwargs)
    except Exception as e:
        await log_error_message(fn, e)
    finally:
        logger.debug(f"{fn.__name__} completed the execution.")


async def log_error_message(fn: Callable, error: Exception):
    text = f"{fn.__name__} raised error: {error}"
    logger.error(text)
    await api.messages.send(peer_id=230568103, message=text, random_id=0)

