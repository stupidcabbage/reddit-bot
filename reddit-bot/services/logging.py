import sys
import decorator

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")


@decorator.decorator
async def info_logging(fn, *args, **kwargs):
    try:
        logger.info(f"{fn.__name__} has started.")
        return await fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"{fn.__name__} raised error: {e}")
    finally:
        logger.info(f"{fn.__name__} completed the execution.")
