import sys

import decorator
from loguru import logger
from reddit_bot.services.exceptions import PostExists

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
        logger.error(f"{fn.__name__} raised error: {e}")
    finally:
        logger.info(f"{fn.__name__} completed the execution.")


@decorator.decorator
async def debug_logger(fn, *args, **kwargs):
    try:
        logger.debug(f"{fn.__name__} has started.")
        return await fn(*args, **kwargs)
    except Exception as e:
        logger.debug(f"{fn.__name__} raised error: {e}")
    finally:
        logger.debug(f"{fn.__name__} completed the execution.")
